#!/bin/sh
# ./build/X86/gem5.opt configs/example/fs.py --caches --l2cache --cpu-type=TimingSimpleCPU --num-cpus=1 --kernel ./vmlinux-4.19.83 --disk-image ./disk-image/boot-exit/boot-exit-image/boot-exit
# ./build/X86/gem5.opt --debug-flags=EnCache configs/example/fs.py --caches --cpu-type=DerivO3CPU --kernel ./vmlinux-5.4.49 --disk-image ./disk-image/boot-exit/boot-exit-image/boot-exit
# ./build/X86/gem5.opt --debug-flags=EnCache gem5-resources/src/boot-exit/configs/run_exit.py --allow_listeners ./vmlinux-4.19.83 ./disk-image/boot-exit-image/boot-exit simple classic 1 init
./build/X86/gem5.opt --debug-flags=EnCache configs/example/fs.py --caches --cpu-type=X86KvmCPU --kernel ./vmlinux-4.19.83 --disk-image ./disk-image/boot-exit/boot-exit-image/boot-exit