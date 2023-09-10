import time
from random import randint

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO_ON=GPIO.HIGH
GPIO_OFF=GPIO.LOW
ON = True
OFF = not ON

# Base clas to Light and Circuit
class Base:
    def __init__(self):
        self.state = False

    def on(self):
        self.state = ON
        return True
    
    def off(self):
        self.state = OFF
        return True
    
    def switch(self):
        return True

# One specific light
class Light (Base):
    def __init__(self, color, pin):
        self.color = color
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self.off()
        super().__init__()
    
    def on(self):
        GPIO.output(self.pin, GPIO_ON)
        super().on()
    
    def off(self):
        GPIO.output(self.pin, GPIO_OFF)
        super().on()

# Circuit of lights 
class Circuit (Base):
    def __init__(self, lights=[]):
        self.lights = lights
        super().__init__()

    def add_light(self, light):
        self.lights.append(light)
    
    def on(self):
        for l in self.lights:
            l.on()
        super().on()
    
    def off(self):
        for l in self.lights:
            l.off()
        super().off()
    
    def on_specific(self, index):
        if index > 1 and index <= self.lights.len():
            self.lights[index-1].on()

    def off_specific(self, index):
        if index > 1 and index <= self.lights.len():
            self.lights[index-1].off()

    def shutdown(self):
        self.off()
        return True

    def run(self, strategy, times):
        for _ in range(times):
            strategy.run(self)

    def print(self):
        print("\n=============================")
        print("IDX\tColor\tPin\tState")
        print("=============================")
        for l in self.lights:
            print(f"{self.lights.index(l)+1}\t{l.color}\t{l.pin}\t{l.state}")

# Strategy Base
class Strategy:
    def __init__(self, delay):
        self.delay = delay
        self.counter = 0

    def reset(self):
        for l in self.lights:
            l.off()

# Light channel one to eight
class Carousel(Strategy):
    def run(self, circuit):
        for l in circuit.lights:
            l.on()
            time.sleep(self.delay)
            l.off()

# Group collors
class SameColor(Strategy):
    def run(self, circuit):
        all_collors = list(set([l.color for l in circuit.lights]))
        for c in all_collors:
            for l in circuit.lights:
                if l.color == c:
                    l.on()
            # circuit.print()
            time.sleep(self.delay)
            for l in circuit.lights:
                if l.color == c:
                    l.off()
    
# Groups blick 10 times
class RandomGroupBlink(Strategy):
    def run(self, circuit):
        amount_of_lights = len(circuit.lights)
        group_size = int(amount_of_lights/2)
        
        for _ in range(5):
            group = []
            for _ in range(group_size):
                l = circuit.lights[randint(0, amount_of_lights-1)]
                group.append(l)
            self.blink_10_times(group)

        return True

    def blink_10_times(self, group):
        for _ in range(10):
            for l in group:
                l.off()
            time.sleep(0.07)
            for l in group:
                l.on()

# Blink all lights
class AllBlink(Strategy):
    def run(self, circuit):
            for l in circuit.lights:
                l.off()
            time.sleep(self.delay)
            for l in circuit.lights:
                l.on()

# Blink Random Lights
class Random(Strategy):
    def run(self, circuit):
        amount_of_lights = len(circuit.lights)
        for _ in range(amount_of_lights):
            l = circuit.lights[randint(0,amount_of_lights-1)]
            l.on()
            time.sleep(0.1)
            l.off()

