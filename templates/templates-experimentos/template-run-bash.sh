#!/bin/bash
mkdir -p result_logs
mkdir -p result_outputs
for valfile in ./valfile_*.val; do
	echo "Run "$valfile
	cat $valfile > valfile.val
	../src/bin/cd++ -mopinion-combined-model.ma -eevents.ev -t{{stop_time}} -llog -ooutput
	cat log07 > result_logs/new_log_${valfile:2:-4}.log
	cat output > result_outputs/new_output_${valfile:2:-4}.out
	rm log*
	rm output
done
rm valfile.val