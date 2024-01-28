#!/bin/bash
echo workqueue:workqueue_queue_work > /sys/kernel/tracing/set_event
cat /sys/kernel/tracing/trace_pipe > workqueue.log 
