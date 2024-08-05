#gentoo
 gcc -march=native -E -v - </dev/null 2>&1 | grep cc1
@output eg:
@`
COMMON_FLAGS="-O2 -march=bonnell \
-mmmx -mno-popcnt -msse -msse2 -msse3 -mssse3 \
-mno-sse4.1 -mno-sse4.2 -mno-avx -mno-avx2 -mno-sse4a -mno-fma4 \
-mno-xop -mno-fma -mno-avx512f -mno-bmi -mno-bmi2 -mno-aes -mno-pclmul -mno-avx512vl \
-mno-avx512bw -mno-avx512dq -mno-avx512cd -mno-avx512er -mno-avx512pf -mno-avx512vbmi -mno-avx512ifma \
-mno-avx5124vnniw -mno-avx5124fmaps -mno-avx512vpopcntdq -mno-avx512vbmi2 -mno-gfni \
-mno-vpclmulqdq -mno-avx512vnni -mno-avx512bitalg -mno-avx512bf16 \
-mno-avx512vp2intersect -mno-3dnow -mno-adx -mno-abm -mno-cldemote -mno-clflushopt -mno-clwb \
-mno-clzero -mcx16 -mno-enqcmd -mno-f16c -mno-fsgsbase -mfxsr -mno-hle \
-msahf -mno-lwp -mno-lzcnt -mmovbe -mno-movdir64b \
-mno-movdiri -mno-mwaitx -mno-pconfig -mno-pku -mno-prefetchwt1 -mno-prfchw \
-mno-ptwrite -mno-rdpid -mno-rdrnd -mno-rdseed -mno-rtm -mno-serialize -mno-sgx -mno-sha \
-mno-shstk -mno-tbm -mno-tsxldtrk -mno-vaes -mno-waitpkg -mno-wbnoinvd \
-mno-xsave -mno-xsavec -mno-xsaveopt -mno-xsaves -mno-amx-tile -mno-amx-int8 -mno-amx-bf16 -mno-uintr \
-mno-hreset -mno-kl -mno-widekl -mno-avxvnni -mno-avx512fp16 -mno-avxifma -mno-avxvnniint8 \
-mno-avxneconvert -mno-cmpccxadd -mno-amx-fp16 -mno-prefetchi -mno-raoint -mno-amx-complex \
--param l1-cache-size=24 --param l1-cache-line-size=64 \
--param l2-cache-size=512 -mtune=bonnell -pipe"
#`


#gentoo < maolang >
{
#make alias ='inhere'
#qlop -t $(qlist -IC) | sort -nk2 }
#
#Literal command line:
alias emergestats='sudo qlop -tgH $(qlist -IC) | sort -nk2'
}
