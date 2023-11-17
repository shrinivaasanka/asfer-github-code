#-------------------------------------------------------------------------------------------------------
#NEURONRAIN ASFER - Software for Mining Large Datasets
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------------
#K.Srinivasan
#NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
#Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/
#--------------------------------------------------------------------------------------------------------

#!/bin/bash
#This script is derived from eBPF bpftrace documentation at https://github.com/iovisor/bpftrace to gather performance
#statistics and observables for the system as a whole, for a process id $1 and for cgroupid $2 - individual stats oneliners
#can be commented or uncommented as deemed necessary

# Profile user-level stacks at 99 Hertz, for PID $1:
bpftrace -e 'profile:hz:99 /pid == $1/ { @[ustack] = count(); }' $1
echo "##############End#Profile#################"

# Files opened, for processes in the root $2 
bpftrace -e 'tracepoint:syscalls:sys_enter_openat /cgroup == cgroupid(str($1))/ { printf("%s\n", str(args->filename)); }' $2
echo "#############End#Files opened in cgroup##################"

# Files opened by process
#bpftrace -e 'tracepoint:syscalls:sys_enter_open { printf("%s %s\n", comm, str(args->filename)); }'
echo "###############################"

# Syscall count by program
#bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }'
echo "###############################"

# Read bytes by process:
#bpftrace -e 'tracepoint:syscalls:sys_exit_read /args->ret/ { @[comm] = sum(args->ret); }'
echo "###############################"

# Read size distribution by process:
#bpftrace -e 'tracepoint:syscalls:sys_exit_read { @[comm] = hist(args->ret); }'
echo "###############################"

# Show per-second syscall rates:
bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @ = count(); } interval:s:1 { print(@); clear(@); }'
echo "###########End#per-second syscall rates####################"

# Trace disk size by process
#bpftrace -e 'tracepoint:block:block_rq_issue { printf("%d %s %d\n", pid, comm, args->bytes); }'
echo "###############################"

# Count page faults by process
#bpftrace -e 'software:faults:1 { @[comm] = count(); }'
echo "###############################"

# Count LLC cache misses by process name and PID (uses PMCs):
#bpftrace -e 'hardware:cache-misses:1000000 { @[comm, pid] = count(); }'
echo "###############################"
