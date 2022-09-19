# boot.py -- run on boot-up
from machine import UART
import machine
import time
import os

uart = UART(0, baudrate=115200)
os.dupterm(uart)

machine.main('abp_node_AU915_scanble.py')
