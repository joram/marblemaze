#!/usr/bin/env python3
import time
import board
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import asyncio


kit = MotorKit(address=0x60, i2c=board.I2C())



class Stepper():

    def __init__(self):
        self.state = False
        self.background_running = False
        self.running = True

    def setState(self, state):
        self.state = state

    def shutdown(self):
        self.running = False

    async def background(self):
        if self.background_running:
            return

        print("starting background stepper task")
        self.background_running
        while self.running:
            if self.state:
                kit.stepper1.onestep()
                await asyncio.sleep(0.001)
            else:
                await asyncio.sleep(1)
        print("stopped background stepper task")
