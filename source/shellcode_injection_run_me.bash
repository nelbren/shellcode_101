#!/bin/bash
#
# shellcode_injection_run_me.bash
#
# v0.0.1 - 2021-09-20 - nelbren@nelbren.com
#

vuln="./vuln"

[ ! -x $vuln ] && ./vuln.bash

cmd[0]="b _start"
cmd[1]="r $(./fill.py)"
cmd[2]="disassemble func"

output=/tmp/output.txt

gdb --batch --quiet -ex "${cmd[0]}" -ex "${cmd[1]}" -ex "${cmd[2]}" $vuln | \
    tee $output

bpoint=$(grep strcpy $output | cut -c4-21)

cmd[0]="b *${bpoint}"
cmd[1]="r $(./fill.py)"
cmd[2]="x/40x \$rsp"
cmd[3]="ni"
cmd[4]="x/40x \$rsp"

gdb --batch --quiet -ex "${cmd[0]}" -ex "${cmd[1]}" -ex "${cmd[2]}" \
    -ex "${cmd[3]}" -ex "${cmd[4]}" $vuln | tee -a $output

begin=$(grep "0x41414141" $output | head -1 | cut -d":" -f1)
end=$(grep "0x42424242" $output | tail -1 | cut -d":" -f1)

./shellcode_injection_find_rip.py $begin $end
