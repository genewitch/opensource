cat ~/afl/ramdisk/out/*/fuzzer_stats |grep cycles |tail -n63| awk '{sum+=$3; count+=1} END {print sum/count}'
