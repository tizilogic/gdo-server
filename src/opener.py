"""
Provides the function to call to open the garage door...
"""

__author__ = 'Tiziano Bettio'
__license__ = 'MIT'
__version__ = '0.1'
__copyright__ = """Copyright (c) 2024 Tiziano Bettio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import time
import threading

from settings import (
    GPIO_PIN, OUTPUT_TIME, CODE_BITS, ZERO_HIGH_US, ZERO_LOW_US,
    ONE_HIGH_US, ONE_LOW_US, PAUSE_US
)

import pigpio


current_state = False

def gen_wave_form():
    wave_form = []
    for c in CODE_BITS:
        if c == '0':
            wave_form += [
                pigpio.pulse(1 << GPIO_PIN, 0, ZERO_HIGH_US),
                pigpio.pulse(0, 1 << GPIO_PIN, ZERO_LOW_US)
            ]
        elif c == '1':
            wave_form += [
                pigpio.pulse(1 << GPIO_PIN, 0, ONE_HIGH_US),
                pigpio.pulse(0, 1 << GPIO_PIN, ONE_LOW_US)
            ]
    wave_form += [pigpio.pulse(0, 1 << GPIO_PIN, PAUSE_US)]
    return wave_form

def open_door():
    lock = threading.Lock()
    lock.acquire()
    global current_state
    if current_state:
        lock.release()
        return
    current_state = True
    lock.release()
    pi = pigpio.pi()
    pi.set_mode(GPIO_PIN, pigpio.OUTPUT)
    pi.wave_clear()
    pi.wave_add_generic(gen_wave_form())
    w = pi.wave_create()
    pi.wave_send_repeat(w)
    time.sleep(OUTPUT_TIME)
    pi.wave_tx_stop()
    pi.wave_clear()
    pi.write(GPIO_PIN, 0)
    lock.acquire()
    current_state = False
    lock.release()
