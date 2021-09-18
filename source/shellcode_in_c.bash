gcc -fno-stack-protector -z execstack -no-pie shellcode_in_c.c -o shellcode_in_c 2>/dev/null
ls -l shellcode_in_c
./shellcode_in_c

