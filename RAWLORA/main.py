# Based in Pycon examples https://github.com/pycom/pycom-libraries/tree/master/examples

from network import LoRa
import socket
import time
import machine

# Initialize LoRa in LORA mode.

# More params can be given, like frequency, tx power and spreading factor.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORA, region=LoRa.US915)

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
#s.setblocking(False)

# send some data
#s.send(bytes([0x01, 0x02, 0x03])

# get any data received...
#data = s.recv(64)
#print(data)

while True:
    # send some data
    s.setblocking(True)
    s.send('Hello')

    # get any data received...
    s.setblocking(False)
    data = s.recv(64)
    print(data)

    # wait a random amount of time
    time.sleep(machine.rng() & 0x0F)
