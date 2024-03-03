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
// #include "rtm.h"
#include "EN.h"
#include <x86intrin.h>

unsigned char key[] =
{
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
  //0x51, 0x4d, 0xab, 0x12, 0xff, 0xdd, 0xb3, 0x32, 0x52, 0x8f, 0xbb, 0x1d, 0xec, 0x45, 0xce, 0xcc, 0x4f, 0x6e, 0x9c,
  //0x2a, 0x15, 0x5f, 0x5f, 0x0b, 0x25, 0x77, 0x6b, 0x70, 0xcd, 0xe2, 0xf7, 0x80
};

char* probe;

int main()
{

  unsigned char plaintext[] =
  {
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  };
  unsigned char ciphertext[128];

  extern const uint32_t Te0[256];
  extern const uint32_t Te3[256];
  // printf("Te0 address: %p\n", Te0);
  // printf("Te3 address: %p\n", Te3);
  char* te0 = (char*)Te0;
  char* te3 = (char*)Te3;

  size_t time;
  size_t delta;

  // void (*func)(const unsigned char *, unsigned char *, const AES_KEY *) = AES_decrypt;

  AES_KEY key_struct;
  AES_set_encrypt_key(key, 128, &key_struct);
  plaintext[0] = 'a';

  int a = 6;

  // ENBEGIN(en_handler, 0);
  // for (probe = te0; probe < te0 + 64*16; probe += 64) {
  //   ENPREFETCH((uint64_t)probe, 1);
  // }
  // ENPREFETCH((uint64_t)te0, 1);
  // _mm_mfence();
  // flush(te0);
  // for(int i=0; i<=1000000; i++);

  // for (probe = a; probe < a + 64*16; probe += 64) {
  //   ENPREFETCH((uint64_t)a, 1);
  // }

  // ENBEGIN(en_handler, 0);
  // ENPREFETCH((uint64_t)&a, 1);
  // // for (probe = te0; probe < te0 + 64*16; probe += 64) {
  // //   ENPREFETCH((uint64_t)probe, 1);
  // // }
  // // _mm_mfence();
  // _mm_clflush(&a);
  // for(int i=0; i<=10000; i++);

  // time = rdtsc();
  // plaintext[0] = j;
  // for(volatile register int j = 0; j < 1; j++){
  //   
  //   flush(a);
  //   _mm_mfence();
  //   AES_encrypt(plaintext, ciphertext, &key_struct);
  // }

  // for (probe = te0; probe < te3 + 64*16; probe += 64) {
  //   _mm_mfence();
  //   flush(probe);
  //   _mm_mfence();
  // }

  // for (probe = te0; probe < te0 + 64*16; probe += 64) // 16    
  //   maccess(probe);

  // _mm_mfence();
  // flush(te0 + 64);
  // _mm_mfence();
  
  time = rdtsc();
  // printf("here\n");
  for (probe = te0; probe < te0 + 64*16; probe += 64)
  {
    // maccess((void *)probe);
    // maccess((void *)(probe+16));
    // maccess((void *)(probe+32));
    // maccess((void *)probe);
    // maccess((void *)(probe+16));
    // maccess((void *)(probe+32));
    *probe;
    *(probe+64);
    *(probe+128);
    *probe;
    *(probe+64);
    *(probe+128);
  }
  delta = rdtsc() - time;
  for(int i=0; i<=10000; i++);

  // AES_encrypt(plaintext, ciphertext, &key_struct);
  // AES_encrypt(plaintext, ciphertext, &key_struct);
  // if (_xbegin() == _XBEGIN_STARTED) {
  //   /* read lock */
  //   /* transaction */
  //   for(volatile register int j = 0; j < 1; j++){
  //     AES_encrypt(plaintext, ciphertext, &key_struct);
  //   }
  //   _xend();
  // }
  // for(volatile register int j = 0; j <= 10000; j++);
  // delta = rdtsc() - time;
  // printf("%lu\n", delta);

  // time = rdtsc();
  // for(volatile register int j = 0; j <= 10000; j++);
  // delta = rdtsc() - time;
  // printf("%lu\n", delta);

  return 0;
}