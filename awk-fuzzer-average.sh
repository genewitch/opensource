cat ~/afl/ramdisk/out/*/fuzzer_stats |grep cycles |tail -n63| awk '{sum+=$3; count+=1} END {print sum/count}'
or 
cat ~/afl/ramdisk/out/djpeg-S*/fuzzer_stats | awk '/cycles/ {sum+=$3; count+=1} END {print sum/count}'
# because the MASTER shouldn't be included, IMO. these are identical commands though
