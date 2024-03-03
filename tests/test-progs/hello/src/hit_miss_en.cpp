#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
#include "EN.h"

uint64_t rdtsc() {
  uint64_t a, d;
  asm volatile ("mfence");
  asm volatile ("rdtsc" : "=a" (a), "=d" (d));
  a = (d<<32) | a;
  asm volatile ("mfence");
  return a;
}

void maccess(void* p)
{
  asm volatile ("movq (%0), %%rax\n"
    :
    : "c" (p)
    : "rax");
}

void flush(void* p) {
    asm volatile ("clflush 0(%0)\n"
      :
      : "c" (p)
      : "rax");
}

void en_handler(en_frame* ef)
{
    /* do something */
    printf("en_frame rip: %p\n", ef->rip);
    __asm__("mov 0x10(%rsp), %rsp");
    __asm__("pop %rcx; pop %rdx; pop %rsi; pop %rdi; pop %r8; pop %r9; pop %r10; pop %r11; pop %r12; pop %r13; pop %r14; pop %r15; pop %rax; pop %rbp; ret"); /* BLACK MAGIC! */
    // __asm__("ret");
    // exit(0);
}

int main(int argc, char** argv) {
    // char* small_buffer = (char*) malloc(1024);
    // char* large_buffer = (char*) malloc(8192);
    int size = atoi(argv[1]);
    int a = 0;
    char* tmp_buffer = (char*) malloc(size);
    char* large_buffer = (char*) malloc(size);
    for (volatile register int j = 0; j < size; ++j) {
        large_buffer[j] = 'a';
        // maccess(large_buffer + j);
    }
    ENBEGIN(en_handler, 0);
    ENPREFETCH((uint64_t)&a);
    for (volatile register int i = 0; i < 20; ++i) {
        maccess(&a);
        size_t time = rdtsc();
        a = 0;
        size_t delta = rdtsc() - time;
        printf("hit: %zu, ", delta);

        // flush(&a);
        for (volatile register int j = 0; j < size; ++j) {
            // maccess(large_buffer + j);
            // maccess(large_buffer + j);
            large_buffer[j] = 'b';
            large_buffer[j] = 'b';
        }
        time = rdtsc();
        a = 0;
        delta = rdtsc() - time;
        printf("evicted: %zu\n", delta);
    }
    free(tmp_buffer);
    free(large_buffer);

    return 0;
}