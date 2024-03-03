# ./build/X86/gem5.opt --debug-flags=EnCache configs/example/se.py --caches --l1i_size='512B' --l1i_assoc=8 --l1d_size='512B' --l1d_assoc=8 --l2cache --l2_size='1kB' --l2_assoc=16 --cpu-type=DerivO3CPU --num-cpus=1 -c /home/fan/en/en-gem5/disk-image/boot-exit/evict_reload/simple 
# ./build/X86/gem5.opt configs/example/se.py --caches --l2cache --cpu-type=DerivO3CPU --num-cpus=1 -c /home/fan/en-gem5-fs/en-gem5/tests/test-progs/en_bench/polybench-c-3.2/en/en/3mm
# ./build/X86/gem5.opt configs/example/se.py --caches --l2cache --cpu-type=DerivO3CPU --num-cpus=1 -c /home/fan/en-gem5-fs/en-gem5/tests/test-progs/en_bench/fr/fr_static
./build/X86/gem5.opt configs/example/se.py --caches --l2cache --cpu-type=DerivO3CPU --num-cpus=1 -c /home/fan/en-gem5-fs/en-gem5/tests/test-progs/en_bench/fr/fr
# ./build/X86/gem5.opt  configs/example/se.py --caches --l2cache --cpu-type=DerivO3CPU --num-cpus=1 -c /home/fan/en-gem5-fs/en-gem5/tests/test-progs/en_bench/fr/aes_no_hw
# ./build/X86/gem5.opt configs/example/se.py --caches --l2cache --cpu-type=DerivO3CPU --num-cpus=1 -c /home/fan/en-gem5-fs/en-gem5/tests/test-progs/en_bench/others/flush_en
# ./build/X86/gem5.opt --debug-flags=EnCache configs/example/se.py -e /home/fan/en/en-gem5/env.sh --caches --l2cache --cpu-type=DerivO3CPU --num-cpus=1 -c /home/fan/Flush-Reload/clflushtest
# ./build/X86/gem5.opt configs/example/se.py -e /home/fan/en/en-gem5/env.sh --caches --l2cache --cpu-type=AtomicSimpleCPU --num-cpus=2 -c /home/fan/Flush-Reload/newspy

# for file in /home/fan/en-gem5-fs/en-gem5/tests/test-progs/en_bench/polybench-c-3.2/en/en/*; do
#     echo "$(basename $file)"
#     # ./time_benchmark.sh $file
#     # ./build/X86/gem5.opt configs/example/se.py --caches --l2cache --l2_size='64kB' --cpu-type=DerivO3CPU --num-cpus=1 -c $file
#     ./build/X86/gem5.opt configs/example/se.py --caches --l1i_size='16kB' --l1d_size='16kB' --l2cache --l2_size='16kB' --cpu-type=DerivO3CPU --num-cpus=1 -c $file
#     # echo
# done