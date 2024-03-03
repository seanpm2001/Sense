# 2mm
# 3mm
# adi
# bicg
# cholesky
# correlation
# covariance
# doitgen
# durbin
# fdtd-2d
# gemm
# gemver
# gesummv
# gramschmidt
# ludcmp
# lu
# mvt
# seidel-2d
# symm
# syr2k
# syrk
# trisolv
# trmm

PARGS1="-mllvm -align-all-functions=8 -mno-red-zone -fomit-frame-pointer -O0 -I utilities -I";
PARGS2="-DMINI_DATASET -DPOLYBENCH_CACHE_SIZE_KB=16";
OUT_DIR1="en/base/";
OUT_DIR2="en/en/";
# for i in `cat en_benchmark_list`; do 
#     mkdir $(dirname $i)_en/; 
#     cp $(dirname $i)/* $(dirname $i)_en/;
# done
for i in `cat en_benchmark_list`; do
    clang $PARGS1 $(dirname $i) utilities/polybench.c "$i" $PARGS2 -o $OUT_DIR1$(basename $(dirname $i)) -lm;
    clang $PARGS1 $(dirname $i)_en/ utilities/polybench.c $(dirname $i)_en/$(basename $i) $PARGS2 -o $OUT_DIR2$(basename $(dirname $i)) -lm;
done

# gcc -O0 -I utilities -I linear-algebra/kernels/atax utilities/polybench.c linear-algebra/kernels/atax/atax.c -DPOLYBENCH_TIME -DSMALL_DATASET -DPOLYBENCH_CACHE_SIZE_KB=4096 -o atax_time
# gcc -O0 -I utilities -I linear-algebra/kernels/2mm utilities/polybench.c linear-algebra/kernels/2mm/2mm.c -DPOLYBENCH_TIME -DSMALL_DATASET -DPOLYBENCH_CACHE_SIZE_KB=4096 -o 2mm_time

# clang -mllvm -align-all-functions=8 -mno-red-zone -fomit-frame-pointer -O0 -I utilities -I linear-algebra/kernels/atax utilities/polybench.c linear-algebra/kernels/atax/atax.c -DPOLYBENCH_TIME -DSMALL_DATASET -DPOLYBENCH_CACHE_SIZE_KB=4096 -o atax_time
# clang -mllvm -align-all-functions=8 -mno-red-zone -fomit-frame-pointer -O0 -I utilities -I ./linear-algebra/kernels/2mm utilities/polybench.c ./linear-algebra/kernels/2mm/2mm.c -DPOLYBENCH_TIME -DPOLYBENCH_CYCLE_ACCURATE_TIMER -DSMALL_DATASET -DPOLYBENCH_CACHE_SIZE_KB=4096 -o 2mm
# clang -mllvm -align-all-functions=8 -mno-red-zone -fomit-frame-pointer -O0 -I utilities -I linear-algebra/kernels/2mm utilities/polybench.c linear-algebra/kernels/2mm/2mm.c -DPOLYBENCH_TIME -DSMALL_DATASET -DPOLYBENCH_CACHE_SIZE_KB=4096 -o 2mm_time

# clang -mllvm -align-all-functions=8 -mno-red-zone -fomit-frame-pointer -O0 -I utilities -I linear-algebra/kernels/atax_en utilities/polybench.c linear-algebra/kernels/atax_en/atax.c -DPOLYBENCH_TIME -DSMALL_DATASET -DPOLYBENCH_CACHE_SIZE_KB=4096 -o en/en/atax_en_time
# clang -mllvm -align-all-functions=8 -mno-red-zone -fomit-frame-pointer -O0 -I utilities -I linear-algebra/kernels/2mm_en utilities/polybench.c linear-algebra/kernels/2mm_en/2mm.c -DPOLYBENCH_TIME -DSMALL_DATASET -DPOLYBENCH_CACHE_SIZE_KB=4096 -o en/en/2mm_en_time

# sudo mount -o loop,offset=1048576  ~/en-gem5-fs/disk-image/boot-exit-image/boot-exit /mnt/iso
# # sudo mkdir /mnt/iso/root/polybench
# sudo cp -r en/ /mnt/iso/root/polybench
# sudo umount /mnt/iso