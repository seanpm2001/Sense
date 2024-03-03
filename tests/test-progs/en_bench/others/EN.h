#include <stdint.h>
#include <cassert>
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

void ENBEGIN(void (*ENHandler)(en_frame*), uint8_t redZoneSize = 128)
{
    uint64_t addr = (uint64_t)(ENHandler);
    //lower 8bits should be clear
    printf("USER: ENBEGIN Handler %lx\n", addr);
    // assert((addr & EN_FLAGS) == 0x00);

    //add red zone size to addr
    addr = addr | (redZoneSize);

    printf("USER: ENBEGIN Handler with redZoneSize %lx\n", addr);
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
void ENPREFETCH(uint64_t addr, uint8_t flags=1)
{

    //lower 8bits should be clear
    // assert(addr & EN_FLAGS);
    //add flags
    printf("USER: ENPREFETCH flags %x\n", flags);
    printf("USER: ENPREFETCH addr  %lx\n", addr);
    
    asm volatile(
		 ".byte 0x0F\n\t"
                 ".byte 0x0C\n\t"
                 :
                 :"a"(addr), "b"(flags)
		 :"memory"
		 );
}
