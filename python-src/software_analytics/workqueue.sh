#!/bin/bash
#mount -t debugfs nodev /sys/kernel/debug
echo workqueue:workqueue_queue_work > /sys/kernel/debug/tracing/set_event
cat /sys/kernel/debug/tracing/trace_pipe > workqueue.log 
sudo awk ' /cpu#/ {cpu=$1} /runnable tasks:/ {show=1; next} /^$/ {show=0} show {print cpu, $0} ' /proc/sched_debug > schedrunqueue.log
