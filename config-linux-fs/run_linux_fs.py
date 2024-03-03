# -*- coding: utf-8 -*-
# Copyright (c) 2019 The Regents of the University of California.
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Jason Lowe-Power, Ayaz Akram, Hoa Nguyen

""" Script to run a SPEC benchmark in full system mode with gem5.

    Inputs:
    * This script expects the following as arguments:
        ** kernel: 
                  This is a positional argument specifying the path to
                  vmlinux.
        ** disk: 
                  This is a positional argument specifying the path to the
                  disk image containing the installed SPEC benchmarks.
        ** cpu: 
                  This is a positional argument specifying the name of the
                  detailed CPU model. The names of the available CPU models
                  are available in the getDetailedCPUModel(cpu_name) function.
                  The function should be modified to add new CPU models.
                  Currently, the available CPU models are:
                    - kvm: this is not a detailed CPU model, ideal for testing.
                    - o3: DerivO3CPU.
                    - atomic: AtomicSimpleCPU.
                    - timing: TimingSimpleCPU.
        ** --allow-listeners:
                  This is an optional argument specifying gem5 to open
                  listening ports. Usually, the ports are opened for debugging
                  purposes. 
                  By default, the ports are off.
"""

import os
import sys

import m5
import m5.ticks
from m5.objects import *

import argparse

from system import MySystem


def parse_arguments():
    parser = argparse.ArgumentParser(description=
                                "gem5 config file to run linux fullsystem")
    parser.add_argument("kernel", type = str, help = "Path to vmlinux")
    parser.add_argument("disk", type = str,
                  help = "Path to the disk image containing SPEC benchmarks")
    parser.add_argument("cpu", type = str, help = "Name of the detailed CPU")
    parser.add_argument("-k", "--kernel", type = str,
                        default = "linux-4.19.83/vmlinux-4.19.83",
                        help = "Path to vmlinux")
    parser.add_argument("-z", "--allow-listeners", default = False,
                        action = "store_true",
                        help = "Turn on ports;"
                               "The ports are off by default")
    return parser.parse_args()

def getDetailedCPUModel(cpu_name):
    '''
    Return the CPU model corresponding to the cpu_name.
    '''
    available_models = {"kvm": X86KvmCPU,
                        "o3": DerivO3CPU,
                        "atomic": AtomicSimpleCPU,
                        "timing": TimingSimpleCPU
                       }
    try:
        available_models["FlexCPU"] = FlexCPU
    except NameError:
        # FlexCPU is not defined
        pass
    # https://docs.python.org/3/library/stdtypes.html#dict.get 
    # dict.get() returns None if the key does not exist
    return available_models.get(cpu_name)

def create_system(linux_kernel_path, disk_image_path, detailed_cpu_model):
    # create the system we are going to simulate
    print (detailed_cpu_model)
    system = MySystem(kernel = linux_kernel_path,
                      disk = disk_image_path,
                      TimingCPUModel = detailed_cpu_model,
                      num_cpus = 1, 
                      no_kvm = False)
    
    system.boot_osflags += ' init=/root/exit.sh'
    # set up the root SimObject and start the simulation
    root = Root(full_system = True, system = system)

    if system.getHostParallel():
        # Required for running kvm on multiple host cores.
        # Uses gem5's parallel event queue feature
        # Note: The simulator is quite picky about this number!
        root.sim_quantum = int(1e9) # 1 ms

    return root, system


def boot_linux():
    '''
    Output 1: False if errors occur, True otherwise
    Output 2: exit cause
    '''
    print("Booting Linux")
    exit_event = m5.simulate()
    exit_cause = exit_event.getCause()
    success = exit_cause == "m5_exit instruction encountered"
    if not success:
        print("Error while booting linux: {}".format(exit_cause))
        exit(1)
    print("Booting done")
    return success, exit_cause

def run_linux_fullsystem():
    print("Start running linux with full system emulation")
    exit_event = m5.simulate()
    exit_cause = exit_event.getCause()
    success = exit_cause == "m5_exit instruction encountered"
    if not success:
        print("Error while running linux: {}".format(exit_cause))
        exit(1)
    print("Emulation done")
    return success, exit_cause

if __name__ == "__m5_main__":
    #for path in sys.path:
    #    print(path)
    #exit(1)
    args = parse_arguments()

    cpu_name = args.cpu
    linux_kernel_path = args.kernel
    disk_image_path = args.disk
    allow_listeners = args.allow_listeners

    output_dir = os.path.join(m5.options.outdir, "speclogs")

    # Get the DetailedCPU class from its name
    detailed_cpu = getDetailedCPUModel(cpu_name)
    if detailed_cpu == None:
        print("'{}' is not define in the config script.".format(cpu_name))
        print("Change getDeatiledCPUModel() in run_spec.py "
              "to add more CPU Models.")
        exit(1)

    root, system = create_system(linux_kernel_path, disk_image_path,
                                 detailed_cpu)

    # needed for long running jobs
    if not allow_listeners:
        m5.disableAllListeners()

    # instantiate all of the objects we've created above
    m5.instantiate()

    # booting linux
    success, exit_cause = boot_linux()

    # reset stats
    print("Reset stats")
    m5.stats.reset()

    # switch from KVM to detailed CPU
    print(system.cpu)
    print(system.detailed_cpu)

    currentCPU = system.cpu
    nextCPU    = system.detailed_cpu
    while (exit_cause == "m5_exit instruction encountered"):
      print("Switching to detailed CPU")
      system.switchCpus(currentCPU, nextCPU)
      print("Switching done")
      success, exit_cause = run_linux_fullsystem()
      temp = currentCPU
      currentCPU = nextCPU
      nextCPU = temp

    # output the stats after running the linux
    print("Output stats")
    m5.stats.dump()

