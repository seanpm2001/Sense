#include <stdint.h>
#include <assert.h>
#include "openssl-1.0.0/include/openssl/aes.h"
#define EN_FLAGS 0xff

typedef unsigned int uword_t __attribute__ ((mode (__word__)));
struct interrupt_frame
{
    uword_t ip;
    uword_t cs;
    uword_t flags;
    uword_t sp;
    uword_t ss;
};

struct en_frame {
    uint64_t paddr;
    uint64_t tid;
    uint64_t rcx;
    uint64_t rdx;
    uint64_t rsi;
    uint64_t rdi;
    uint64_t r8;
    uint64_t r9;
    uint64_t r10;
    uint64_t r11;
    uint64_t r12;
    uint64_t r13;
    uint64_t r14;
    uint64_t r15;
    uint64_t rax;
    uint64_t rbp;
    uint64_t rip;
};

void ENBEGIN(void (*)(struct en_frame*), uint8_t);

void ENPREFETCH(uint64_t, uint8_t);

// void en_handler(struct en_frame* ef)
// {
//     /* do something */
//     // printf("user en_handler: Thread %i evicted paddr %p\n", (int)ef->tid, ef->paddr);
//     // printf("at user en_handler\n");
//     // ENBEGIN(en_handler, 0);
//     // asm volatile ("mfence");
//     // printf("en_frame rip: %p\n", ef->rip);
//     // printf("In handler!\n");
//     if ((int)ef->tid != 1)
//         ;
//     if (ef->paddr != 0)
//         ;
//     asm volatile ("mfence");
//     __asm__("mov (%rsp), %rsp");
//     __asm__("pop %rcx; pop %rcx; pop %rcx; pop %rdx; pop %rsi; pop %rdi; pop %r8; pop %r9; pop %r10; pop %r11; pop %r12; pop %r13; pop %r14; pop %r15; pop %rax; pop %rbp; ret"); /* BLACK MAGIC! */
//     // __asm__("ret");
//     // exit(0);
// }

extern const uint32_t Te0[256];
extern const uint32_t Te3[256];
char* te0 = (char*)Te0;
char* te3 = (char*)Te3;
char a[256] = "";

void en_handler(en_frame* ef)
{
    // printf("here\n");
    /* do something */
    ENBEGIN(en_handler, 0);
    // ENPREFETCH((uint64_t)&a, 1);
    for (char* probe = te3; probe < te3 + 64*16; probe += 64) {
        ENPREFETCH((uint64_t)probe, 1);
    }
    
    // printf("user en_handler: enter EN mode\n");
    // printf("user en_handler: Thread %i evicted paddr %p\n", (int)ef->tid, ef->paddr);
    // printf("en_frame rip: %p\n", ef->rip);
    // for (volatile register int i = 0; i < 10000; i++);
    // asm volatile ("mfence");
    __asm__("mov 0x10(%rsp), %rsp");
    __asm__("pop %rcx; pop %rcx; pop %rcx; pop %rdx; pop %rsi; pop %rdi; pop %r8; pop %r9; pop %r10; pop %r11; pop %r12; pop %r13; pop %r14; pop %r15; pop %rax; pop %rbp; ret"); /* BLACK MAGIC! */
    // __asm__("ret");
    // exit(0);
}

void ENBEGIN(void (*ENHandler)(struct en_frame*), uint8_t redZoneSize)
{
    uint64_t addr = (uint64_t)(ENHandler);
    //lower 8bits should be clear
    // printf("USER: ENBEGIN Handler %lx\n", addr);
    // assert((addr & EN_FLAGS) == 0x00);

    //add red zone size to addr
    addr = addr | (redZoneSize);

    // printf("USER: ENBEGIN Handler with redZoneSize %lx\n", addr);
    asm volatile(".byte 0x0F\n\t"
                 ".byte 0x0A\n\t"
                 :
                 :"a"(addr));
}

void ENEND()
{
    asm volatile(".byte 0x0F\n\t"
                 ".byte 0x0B\n\t");
}


//XXX:flags 1 -> cache , flags 2 -> TLB
void ENPREFETCH(uint64_t addr, uint8_t flags)
{
    flags = 1;
    //lower 8bits should be clear
    // assert(addr & EN_FLAGS);
    //add flags
    // printf("USER: ENPREFETCH flags %x\n", flags);
    // printf("USER: ENPREFETCH addr  %lx\n", addr);
    
    asm volatile(
		 ".byte 0x0F\n\t"
                 ".byte 0x0C\n\t"
                 :
                 :"a"(addr), "b"(flags)
		 :"memory"
		 );
}
