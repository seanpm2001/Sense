/*
 * Copyright (c) 2006 The Regents of The University of Michigan
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * Authors: Steve Reinhardt
 */

#include <stdio.h>
#include <stdlib.h>
#include "EN.h"
#include <x86intrin.h>
#include <unistd.h>
#include <malloc.h>

// struct en_frame {
//     uint64_t rcx;
//     uint64_t rdx;
//     uint64_t rsi;
//     uint64_t rdi;
//     uint64_t r8;
//     uint64_t r9;
//     uint64_t r10;
//     uint64_t r11;
//     uint64_t r12;
//     uint64_t r13;
//     uint64_t r14;
//     uint64_t r15;
//     uint64_t rax;
//     uint64_t rbp;
// };

inline void clflush(volatile void *p)
{
    printf("Flushing the EN cache\n");
    asm volatile ("clflush (%0)" :: "r"(p));
}
 
__attribute__ ((interrupt))
void en_handler(struct interrupt_frame *frame)
{
    /* do something */
    printf("ENhandler successfully invoked\n");
}

void enHandler1(en_frame* ef)
{
    /* do something */
    printf("preparation en_frame rip: %p\n", ef->rip);
    __asm__("mov 0x10(%rsp), %rsp");
    __asm__("pop %rcx; pop %rdx; pop %rsi; pop %rdi; pop %r8; pop %r9; pop %r10; pop %r11; pop %r12; pop %r13; pop %r14; pop %r15; pop %rax; pop %rbp; ret"); /* BLACK MAGIC! */
    // __asm__("ret");
    // exit(0);
}

void enHandler2(en_frame* ef)
{
    /* do something */
    printf("execution en_frame rip: %p\n", ef->rip);
    __asm__("mov 0x10(%rsp), %rsp");
    __asm__("pop %rcx; pop %rdx; pop %rsi; pop %rdi; pop %r8; pop %r9; pop %r10; pop %r11; pop %r12; pop %r13; pop %r14; pop %r15; pop %rax; pop %rbp; ret"); /* BLACK MAGIC! */
    // __asm__("ret");
    // exit(0);
}

void test_int()
{
    int var = 6;
    printf("hello world to test EN int\n");
    printf("stack address of %d is :%p\n", var, &var);
    ENBEGIN(enHandler1, 0);
    ENPREFETCH((uint64_t)&var);
    printf("Preparation phase\n");
    _mm_mfence();
    // _mm_clflush(&var);
    // _mm_mfence();
    // sleep(1);
    for(int i=0; i<=10000; i++);
    ENBEGIN(enHandler2, 0);
    ENPREFETCH((uint64_t)&var);
    printf("Flushing the EN cache during execution\n");
    _mm_mfence();
    _mm_clflush(&var);
    for(int i=0; i<=10000; i++);
    printf("After flushing the EN cache\n");
}

void test_array()
{
    // char *p;
    // int pagesize;
    // pagesize = sysconf(_SC_PAGE_SIZE);
    // p = static_cast<char*>(memalign(pagesize, pagesize));
    char p[1024]; 
    printf("hello world to test EN array\n");
    printf("stack address of %d is :%p\n", *p, p);
    ENBEGIN(enHandler1, 0);
    ENPREFETCH((uint64_t)p);
    printf("Preparation phase\n");
    _mm_mfence();
    for(int i=0; i<=10000; i++);
    ENBEGIN(enHandler2, 0);
    ENPREFETCH((uint64_t)p);
    printf("Flushing the EN cache during execution\n");
    _mm_mfence();
    _mm_clflush(p);
    for(int i=0; i<=10000; i++);
    printf("After flushing the EN cache\n");
}

void test_no_en()
{
    // char *p;
    // int pagesize;
    // pagesize = sysconf(_SC_PAGE_SIZE);
    // p = static_cast<char*>(memalign(pagesize, pagesize));
    char p[1024]; 
    printf("Flushing the cache during execution\n");
    _mm_mfence();
    _mm_clflush(p);
    for(int i=0; i<=10000; i++);
    printf("After flushing the cache\n");
}

int main(int argc, char* argv[])
{
    test_array();
    return 0;
}

