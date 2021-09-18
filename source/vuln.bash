gcc vuln.c -o vuln -fno-stack-protector -z execstack
ls -l vuln
./vuln Nelbren
