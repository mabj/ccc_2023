#!/usr/bin/python
import os
import sys

import signal

from random import randint

MAIN_PATH=os.path.dirname(os.path.abspath(__file__))
LIB_PATH=os.path.join(MAIN_PATH, 'lib')
sys.path.append(LIB_PATH)

from entity import Light, Circuit, Carousel, SameColor, AllBlink, RandomGroupBlink, Random

# INITIALIZING LIGHT BULBS
lights = []

lights.append(Light('green', 16))
lights.append(Light('green', 15))

lights.append(Light('purple', 13))
lights.append(Light('purple', 11))

lights.append(Light('orange', 22))
lights.append(Light('orange', 36))

lights.append(Light('red', 37))
lights.append(Light('red', 18))

# Adding lights to circuit
circuit = Circuit(lights)

strategies = [
    Carousel(0.008),
    SameColor(0.1),
    RandomGroupBlink(0.04),
    AllBlink(0.05),
    Carousel(0.1),
    Random(0.8)
]

def signal_handler(sig, frame):
    print("[+] CTRL+C was pressed. Turning off the circuit cleanly.")
    global circuit
    circuit.off()

    circuit.shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    idx = randint(0,len(strategies)-1)
    how_many_times = randint(4,8)
    strategy = strategies[idx]
    print(f"[+] Strategy \"{strategy.__class__.__name__}\" ({how_many_times} times)")
    circuit.run(strategy, how_many_times)
