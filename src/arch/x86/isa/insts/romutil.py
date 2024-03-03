wq# Copyright (c) 2008 The Regents of The University of Michigan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Gabe Black

intCodeTemplate = '''
def rom
{
    # This vectors the CPU into an interrupt handler in long mode.
    # On entry, t1 is set to the vector of the interrupt and t7 is the current
    # ip. We need that because rdip returns the next ip.
    extern %(startLabel)s:

    #
    # Get the 64 bit interrupt or trap gate descriptor from the IDT
    #

    # Load the gate descriptor from the IDT
    slli t4, t1, 4, dataSize=8
    ld t2, idtr, [1, t0, t4], 8, dataSize=8, addressSize=8, atCPL0=True
    ld t4, idtr, [1, t0, t4], dataSize=8, addressSize=8, atCPL0=True

    # Make sure the descriptor is a legal gate.
    chks t1, t4, %(gateCheckType)s

    #
    # Get the target CS descriptor using the selector in the gate
    # descriptor.
    #
    srli t10, t4, 16, dataSize=8
    andi t5, t10, 0xF8, dataSize=8
    andi t0, t10, 0x4, flags=(EZF,), dataSize=2
    br rom_local_label("%(startLabel)s_globalDescriptor"), flags=(CEZF,)
    ld t3, tsl, [1, t0, t5], dataSize=8, addressSize=8, atCPL0=True
    br rom_local_label("%(startLabel)s_processDescriptor")
%(startLabel)s_globalDescriptor:
    ld t3, tsg, [1, t0, t5], dataSize=8, addressSize=8, atCPL0=True
%(startLabel)s_processDescriptor:
    chks t10, t3, IntCSCheck, dataSize=8
    wrdl hs, t3, t10, dataSize=8

    # Stick the target offset in t9.
    wrdh t9, t4, t2, dataSize=8


    #
    # Figure out where the stack should be
    #

    # Record what we might set the stack selector to.
    rdsel t11, ss

    # Check if we're changing privelege level. At this point we can assume
    # we're going to a DPL that's less than or equal to the CPL.
    rdattr t10, hs, dataSize=8
    andi t10, t10, 3, dataSize=8
    rdattr t5, cs, dataSize=8
    andi t5, t5, 0x3, dataSize=8
    sub t0, t5, t10, flags=(EZF,), dataSize=8
    # We're going to change priviledge, so zero out the stack selector. We
    # need to let the IST have priority so we don't branch yet.
    mov t11, t0, t0, flags=(nCEZF,)

    # Check the IST field of the gate descriptor
    srli t12, t4, 32, dataSize=8
    andi t12, t12, 0x7, dataSize=8
    subi t0, t12, 1, flags=(ECF,), dataSize=8
    br rom_local_label("%(startLabel)s_istStackSwitch"), flags=(nCECF,)
    br rom_local_label("%(startLabel)s_cplStackSwitch"), flags=(nCEZF,)

    # If we're here, it's because the stack isn't being switched.
    # Set t6 to the new aligned rsp.
    mov t6, t6, rsp, dataSize=8
    br rom_local_label("%(startLabel)s_stackSwitched")

%(startLabel)s_istStackSwitch:
    ld t6, tr, [8, t12, t0], 0x1c, dataSize=8, addressSize=8, atCPL0=True
    br rom_local_label("%(startLabel)s_stackSwitched")

%(startLabel)s_cplStackSwitch:
    # Get the new rsp from the TSS
    ld t6, tr, [8, t10, t0], 4, dataSize=8, addressSize=8, atCPL0=True

%(startLabel)s_stackSwitched:

    andi t6, t6, 0xF0, dataSize=1
    subi t6, t6, 40 + %(errorCodeSize)d, dataSize=8

    ##
    ## Point of no return.
    ## We're now going to irrevocably modify visible state.
    ## Anything bad that's going to happen should have happened by now or will
    ## happen right now.
    ##
    wrip t0, t9, dataSize=8

    #
    # Set up the target code segment. Do this now so we have the right
    # permissions when setting up the stack frame.
    #
    srli t5, t4, 16, dataSize=8
    andi t5, t5, 0xFF, dataSize=8
    wrdl cs, t3, t5, dataSize=8
    # Tuck away the old CS for use below
    limm t10, 0, dataSize=8
    rdsel t10, cs, dataSize=2
    wrsel cs, t5, dataSize=2

    # Check that we can access everything we need to on the stack
    ldst t0, hs, [1, t0, t6], dataSize=8, addressSize=8
    ldst t0, hs, [1, t0, t6], \
         32 + %(errorCodeSize)d, dataSize=8, addressSize=8


    #
    # Build up the interrupt stack frame
    #


    # Write out the contents of memory
    %(errorCodeCode)s
    st t7, hs, [1, t0, t6], %(errorCodeSize)d, dataSize=8, addressSize=8
    st t10, hs, [1, t0, t6], 8 + %(errorCodeSize)d, dataSize=8, addressSize=8
    rflags t10, dataSize=8
    st t10, hs, [1, t0, t6], 16 + %(errorCodeSize)d, dataSize=8, addressSize=8
    st rsp, hs, [1, t0, t6], 24 + %(errorCodeSize)d, dataSize=8, addressSize=8
    rdsel t5, ss, dataSize=2
    st t5, hs, [1, t0, t6], 32 + %(errorCodeSize)d, dataSize=8, addressSize=8

    # Set the stack segment
    mov rsp, rsp, t6, dataSize=8
    wrsel ss, t11, dataSize=2

    #
    # Adjust rflags which is still in t10 from above
    #

    # Set IF to the lowest bit of the original gate type.
    # The type field of the original gate starts at bit 40.

    # Set the TF, NT, and RF bits. We'll flip them at the end.
    limm t6, (1 << 8) | (1 << 14) | (1 << 16), dataSize=8
    or t10, t10, t6, dataSize=8
    srli t5, t4, 40, dataSize=8
    srli t7, t10, 9, dataSize=8
    xor t5, t7, t5, dataSize=8
    andi t5, t5, 1, dataSize=8
    slli t5, t5, 9, dataSize=8
    or t6, t5, t6, dataSize=8

    # Put the results into rflags
    wrflags t6, t10

    eret
};
'''

microcode = \
intCodeTemplate % {\
    "startLabel" : "longModeInterrupt",
    "gateCheckType" : "IntGateCheck",
    "errorCodeSize" : 0,
    "errorCodeCode" : ""
} + \
intCodeTemplate % {\
    "startLabel" : "longModeSoftInterrupt",
    "gateCheckType" : "SoftIntGateCheck",
    "errorCodeSize" : 0,
    "errorCodeCode" : ""
} + \
intCodeTemplate % {\
    "startLabel" : "longModeInterruptWithError",
    "gateCheckType" : "IntGateCheck",
    "errorCodeSize" : 8,
    "errorCodeCode" : '''
    st t15, hs, [1, t0, t6], dataSize=8, addressSize=8
    '''
} + \
'''
def rom
{
    # This vectors the CPU into an interrupt handler in legacy mode.
    extern legacyModeInterrupt:
    panic "Legacy mode interrupts not implemented (in microcode)"
    eret
};

def rom
{
    extern initIntHalt:
    rflags t1
    limm t2, "~IFBit"
    and t1, t1, t2
    wrflags t1, t0
    halt
    eret
};

def rom
{
    #t1: Which address has been monitored?
    #t7: interrupting PC address, #t15: Errorcode 
    #t13: tid causing the fault
    #t14: physicall address of the affected memory
    extern longModeEventNotifier:

    #read EVENT_NOTIFIER register
    rdval t2, "InstRegIndex(MISCREG_EVENT_NOTIFIER)", dataSize=1

    # # unset interrupt/exception helper register
    # xor t0, t0, t0
    # wrval "InstRegIndex(MISCREG_EVENT_NOTIFIER_INT_EX)", t0, dataSize=1

    #t3: redzone size, #t4: handler address
    ##retrieve redzone size 
    andi t3, t2, 255, dataSize=1
    ##retrieve handler adderss
    sub t4, t2, t3, dataSize=8

    #relocate RSP to avoid redzone
    sub rsp, rsp, t3, dataSize=8

    #For Rom code, Null Environment is used
    #store interrupted rip for return later 
    # st t7, ss, [1, t0, rsp], "1 * -8", dataSize=8, addressSize=8
    # subi rsp, rsp, "1 * 8"

    # rdip t7
    # Check target of call
    st t7, ss, [1, t0, rsp], "1 * -8", dataSize=8, addressSize=8
    subi rsp, rsp, "1 * 8", dataSize=8

    # #store interrupted context
    # st rax, ss, [1, t0, rsp], "1 * -8", dataSize=8, addressSize=8
    # st rcx, ss, [1, t0, rsp], "2 * -8", dataSize=8, addressSize=8
    # st rdx, ss, [1, t0, rsp], "3 * -8", dataSize=8, addressSize=8
    # st rbx, ss, [1, t0, rsp], "4 * -8", dataSize=8, addressSize=8
    # st rsp, ss, [1, t0, rsp], "5 * -8", dataSize=8, addressSize=8
    # st rbp, ss, [1, t0, rsp], "6 * -8", dataSize=8, addressSize=8
    # st rsi, ss, [1, t0, rsp], "7 * -8", dataSize=8, addressSize=8
    # st rdi, ss, [1, t0, rsp], "8 * -8", dataSize=8, addressSize=8
    # subi rsp, rsp, "8 * 8"

    # struct en_frame {
    #     uint64_t paddr;
    #     uint64_t tid;
    #     uint64_t rcx;
    #     uint64_t rdx;
    #     uint64_t rsi;
    #     uint64_t rdi;
    #     uint64_t r8;
    #     uint64_t r9;
    #     uint64_t r10;
    #     uint64_t r11;
    #     uint64_t r12;
    #     uint64_t r13;
    #     uint64_t r14;
    #     uint64_t r15;
    #     uint64_t rax;
    #     uint64_t rbp;
    # };
    # cda ss, [1, t0, rsp], "-8", dataSize=ssz
    # cda ss, [1, t0, rsp], "-10 * 8", dataSize=8
    st rbp, ss, [1, t0, rsp], "1 * -8", dataSize=8, addressSize=8
    st rax, ss, [1, t0, rsp], "2 * -8", dataSize=8, addressSize=8
    st r15, ss, [1, t0, rsp], "3 * -8", dataSize=8, addressSize=8
    st r14, ss, [1, t0, rsp], "4 * -8", dataSize=8, addressSize=8
    st r13, ss, [1, t0, rsp], "5 * -8", dataSize=8, addressSize=8
    st r12, ss, [1, t0, rsp], "6 * -8", dataSize=8, addressSize=8
    st r11, ss, [1, t0, rsp], "7 * -8", dataSize=8, addressSize=8
    st r10, ss, [1, t0, rsp], "8 * -8", dataSize=8, addressSize=8
    st r9, ss, [1, t0, rsp], "9 * -8", dataSize=8, addressSize=8
    st r8, ss, [1, t0, rsp], "10 * -8", dataSize=8, addressSize=8
    st rdi, ss, [1, t0, rsp], "11 * -8", dataSize=8, addressSize=8
    st rsi, ss, [1, t0, rsp], "12 * -8", dataSize=8, addressSize=8
    st rdx, ss, [1, t0, rsp], "13 * -8", dataSize=8, addressSize=8
    st rcx, ss, [1, t0, rsp], "14 * -8", dataSize=8, addressSize=8
    # for sending tid -> paddr data for cache coloring
    st t13, ss, [1, t0, rsp], "15 * -8", dataSize=8, addressSize=8
    st t14, ss, [1, t0, rsp], "16 * -8", dataSize=8, addressSize=8
    subi rsp, rsp, "16 * 8", dataSize=8
    # store rsp (pop rsp works as rsp + 8 -> rsp - 8)
    # subi rsp, rsp, "1 * 8"
    # st rsp, ss, [1, t0, rsp], "1 * -8", dataSize=8, addressSize=8
    # store rsp to rdi
    # st rsp, ds, [1, t0, rdi], dataSize=8, addressSize=8
    # limm rdi, 4
    mov rdi, rsp, rsp, dataSize=8

    #jump to ENHandler address
    #wrip t0, t4, dataSize=8
    wrip t0, t4, dataSize=8
    eret
};
'''
