"""
Provides the function to call to open the garage door...
"""

__author__ = 'Tiziano Bettio'
__license__ = 'MIT'
__version__ = '0.1'
__copyright__ = """Copyright (c) 2019 Tiziano Bettio

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

from settings import GPIO_PIN
from settings import OUTPUT_TIME

try:
    import RPi.GPIO as GPIO
except ImportError:
    class Dummy(object):
        BOARD = None
        OUT = None

        def cleanup(self):
            pass

        def setmode(self, *args, **kwargs):
            pass

        def setup(self, *args, **kwargs):
            pass

        def output(self, *args, **kwargs):
            pass
    GPIO = Dummy()


GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

current_state = False


def open_door():
    lock = threading.Lock()
    lock.acquire()
    global current_state
    if current_state:
        lock.release()
        return
    current_state = True
    lock.release()
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    GPIO.output(GPIO_PIN, True)
    time.sleep(OUTPUT_TIME)
    GPIO.output(GPIO_PIN, False)
    lock.acquire()
    current_state = False
    lock.release()
