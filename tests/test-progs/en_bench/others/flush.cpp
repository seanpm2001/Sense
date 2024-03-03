#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
#include <x86intrin.h>

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

int main(int argc, char** argv) {
    // char* small_buffer = (char*) malloc(1024);
    // char* large_buffer = (char*) malloc(8192);
    // printf("user application starts.\n");
    int a = 0;
    for (volatile register int i = 0; i < 20; ++i) {
        a = 0;
        _mm_mfence();
        size_t time = rdtsc();
        maccess(&a);
        size_t delta = rdtsc() - time;
        printf("hit: %zu, ", delta);
        // printf("round %d\n", i);
        // printf("triggering eviction...\n");
        _mm_mfence();
        flush(&a);
        _mm_mfence();
        // for(volatile register int j = 0; j <= 10000; j++);
        time = rdtsc();
        maccess(&a);
        delta = rdtsc() - time;
        printf("miss: %zu\n", delta);
    }
    // printf("user application ends.\n");

    return 0;
}