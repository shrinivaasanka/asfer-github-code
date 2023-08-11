#!/bin/bash
strace -f -e read -p $1 2> ./asfer_syscall_trace.log
#ltrace -c -p $1 2> ./asfer_syscall_trace.log

