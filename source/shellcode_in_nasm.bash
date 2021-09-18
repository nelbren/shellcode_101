nasm -f elf64 shellcode_in_nasm.asm -o shellcode_in_nasm.o
ld shellcode_in_nasm.o -o shellcode_in_nasm
ls -l shellcode_in_nasm
objdump -d -j .text -M intel shellcode_in_nasm
./shellcode_in_nasm
