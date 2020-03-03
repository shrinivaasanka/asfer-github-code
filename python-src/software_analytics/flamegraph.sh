perf record -g dd if=/dev/zero of=test.data count=10 bs=1M
cp perf.data perf.data.dd
perf script -i perf.data.dd | /media/Ubuntu2/FlameGraph/stackcollapse-perf.pl > out.dd.folded
/media/Ubuntu2/FlameGraph/flamegraph.pl out.dd.folded > out.perf.dd.svg
