#!/bin/sh

# build/X86/gem5.opt --debug-flags=EnCache configs/learning_gem5/part1/two_level.py --l2_size='1MB' --l1d_size='128kB' /home/fan/en/en-gem5/tests/test-progs/hello/bin/x86/linux/hello

 build/X86/gem5.opt --debug-flags=EnCache configs/learning_gem5/part1/two_level.py --l2_size='1MB' --l1d_size='128kB' /home/fan/en/en-gem5/tests/test-progs/hello/src/hello

