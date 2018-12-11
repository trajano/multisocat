#!/usr/bin/env python3
import os
import subprocess
import signal

processes = []
for key in os.environ.keys():
    if key.startswith("SOCAT_"):
        processes.append(
            subprocess.Popen(["socat"] + os.environ.get(key).split(" ")))
    elif key == "BLACKHOLE_TCP":
        for port in os.environ.get(key).split(","):
            processes.append(
                subprocess.Popen(["nc", "-l", port]))
    elif key == "BLACKHOLE_UDP":
        for port in os.environ.get(key).split(","):
            processes.append(
                subprocess.Popen(["nc", "-ul", port]))


def terminate_processes():
    for process in processes:
        process.terminate()


signal.signal(signal.SIGTERM, terminate_processes)

for process in processes:
    process.wait()
