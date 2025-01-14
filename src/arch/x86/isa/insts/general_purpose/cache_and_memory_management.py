# Copyright (c) 2007 The Hewlett-Packard Development Company
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
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

microcode = '''

def macroop ENBEGIN
{
    wrval "InstRegIndex(MISCREG_EVENT_NOTIFIER)", rax
    # limm "InstRegIndex(MISCREG_EVENT_NOTIFIER_MODE)", 1
    # limm "InstRegIndex(MISCREG_EVENT_NOTIFIER_INT_EX)", 0
    # xor t0, t0, t0
    # wrval "InstRegIndex(MISCREG_EVENT_NOTIFIER_INT_EX)", t0
    # addi t0, t0, 1
    # wrval "InstRegIndex(MISCREG_EVENT_NOTIFIER_MODE)", t0
};

def macroop ENEND
{
    xor t0, t0, t0
    wrval "InstRegIndex(MISCREG_EVENT_NOTIFIER)", t0
};

def macroop PREFETCH_EN
{
    subi t0, rbx, 1, flags=(ZF,), dataSize=1
    br label("prefetch_cache"), flags=(CZF,)

    subi t0, rbx, 2, flags=(ZF,), dataSize=1
    br label("prefetch_tlb"), flags=(CZF,)

    br label("prefetch_end")

##    rdval t2, "InstRegIndex(MISCREG_EVENT_NOTIFIER_DESC)", dataSize=1
##    ori t2, t2, 0x2
##    wrval "InstRegIndex(MISCREG_EVENT_NOTIFIER_DESC)", t2, dataSize=1
prefetch_tlb:
    ld t0, seg, [1, rax, t0], disp, dataSize=1, EnCache=False, EnTlb=True
    br label("prefetch_end")

prefetch_cache:
    ld t0, seg, [1, rax, t0], disp, dataSize=1, EnCache=True, EnTlb=False

prefetch_end:
    fault "NoFault"
};

def macroop PREFETCH_M
{
    ld t0, seg, sib, disp, dataSize=1, prefetch=True
};

def macroop PREFETCH_P
{
    rdip t7
    ld t0, seg, riprel, disp, dataSize=1, prefetch=True
};

def macroop PREFETCH_T0_M
{
    ld t0, seg, sib, disp, dataSize=1, prefetch=True
};

def macroop PREFETCH_T0_P
{
    rdip t7
    ld t0, seg, riprel, disp, dataSize=1, prefetch=True
};

def macroop CLFLUSH_M
{
    clflushopt t0, seg, sib, disp, dataSize=1
    mfence
};

def macroop CLFLUSH_P
{
    rdip t7
    clflushopt t0, seg, riprel, disp, dataSize=1
    mfence
};

def macroop CLFLUSHOPT_M
{
    clflushopt t0, seg, sib, disp, dataSize=1
};

def macroop CLFLUSHOPT_P
{
    rdip t7
    clflushopt t0, seg, riprel, disp, dataSize=1
};

def macroop CLWB_M
{
    clwb t1, seg, sib, disp, dataSize=1
};

def macroop CLWB_P
{
    rdip t7
    clwb t1, seg, riprel, disp, dataSize=1
};

'''

#let {{
#    class LFENCE(Inst):
#       "GenFault ${new UnimpInstFault}"
#    class SFENCE(Inst):
#       "GenFault ${new UnimpInstFault}"
#    class MFENCE(Inst):
#       "GenFault ${new UnimpInstFault}"
#    class PREFETCHlevel(Inst):
#       "GenFault ${new UnimpInstFault}"
#    class PREFETCHW(Inst):
#       "GenFault ${new UnimpInstFault}"
#}};
