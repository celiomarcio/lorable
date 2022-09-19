# Based in Pycon examples https://github.com/pycom/pycom-libraries/tree/master/examples

from network import LoRa
from network import Bluetooth
import socket
import binascii
import struct
import time
import config


# Data Structure for IOTAPP or BLE targets
def index_2d(data, search):
    for i, e in enumerate(data):
        try:
            return i, e.index(search)
        except ValueError:
            pass
    raise ValueError("{} is not in list".format(repr(search)))

# initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AU915)

# create an ABP authentication params
#dev_addr = struct.unpack(">l", binascii.unhexlify('2601147D'))[0]
dev_addr = struct.unpack(">l", binascii.unhexlify('2601147d'))[0]
nwk_swkey = binascii.unhexlify('3C74F4F40CAEA021303BC24284FCF3AF')
app_swkey = binascii.unhexlify('0FFA7072CC6FF69A102A0F39BEB0880F')

# remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

# set the 3 default channels to the same frequency
lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)

# make the socket non-blocking
s.setblocking(False)

#Iniciando BLE
bt = Bluetooth()
bt.stop_scan()

#List of Attributes of Interest defined by IotApp
# Tuple topic, mac, service, feature
#0         name     ,  b'b827eba88fd7', int('0x1800',16),         10752
##my_mac = b'b827eba88fd7'
##my_service = int('0x1800',16)
##my_characteristic = 10752

# Features
# Topic, Mac, Service UUID , Caracteristica UUID
# After scanning these are the topics that interest the Iot App
arr = []
arr.append([])
#line=0
#arr[line].append('name')
#arr[line].append(b'b827eba88fd7')
#arr[line].append(int('0x1800',16))
#arr[line].append(10752)
#MIband1 (real device)
line=0
arr[line].append('name')
arr[line].append(b'880f1030f414')
arr[line].append(int('0x1800',16))
arr[line].append(10756)
arr.append([])
line=1
arr[line].append('name')
arr[line].append(b'7c76355ce8fa')
arr[line].append(int('0x1800',16))
arr[line].append(10752)
arr.append([])
line=2
arr[line].append('name')
arr[line].append(b'c855adebcd3a')
arr[line].append(int('0x1800',16))
arr[line].append(int('0x2a00',16))
#

bt.start_scan(-1)

while True:
    time.sleep(5)
    print ("Capturing advisors ...")
    adv = bt.get_adv()
    if bt.isscanning():
        print(adv)
    else:
        bt.start_scan(-1)
    if adv:#.mac == 'b827eba88fd7':
        # try to get the complete name
        #print(bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL))

        # try to get the manufacturer data (Apple's iBeacon data is sent here)
        name = bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
        #mfg_data = bt.resolve_adv_data(adv.data, Bluetooth.ADV_MANUFACTURER_DATA)

        #if mfg_data:
            # try to get the manufacturer data (Apple's iBeacon data is sent here)
            #print(binascii.hexlify(mfg_data))
        try:
            position = index_2d(arr, binascii.hexlify(adv.mac)) # (4, 3)
            print("Finding Index of ...")
            print(adv.mac)
            print("Position Index Found...")
            print(arr[position[0]][position[1]])
        except:
            continue

        if adv.mac != binascii.unhexlify(arr[position[0]][position[1]]):
            print('skipping {} {}'.format(binascii.hexlify(adv.mac), name))
            continue
        #if bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL):
        print(bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL))

        try:
            conn = bt.connect(adv.mac)
        except:
            continue
        services = conn.services()
        for service in services:
            time.sleep(0.350)
            print (service.uuid())
            if service.uuid() == arr[position[0]][2]:
                print ("Position service is ..")
                print (arr[position[0]][2])
                if type(service.uuid()) == bytes:
                    print('Reading chars from bytes service = {}'.format(service.uuid()))
                    print(service.uuid())
                else:
                    print('Reading chars from hex service = %x' % service.uuid())
                    print(service.uuid())
                    print(service.characteristics())
                time.sleep(0.350)
                try:
                    chars = service.characteristics()
                #except:
                #conn.disconnect()
                #bt.start_scan(-1)
                #    continue
                #try:
                    for char in chars:
                        print("UUID")
                        print(char.uuid())
                        print("---")
                        if type(char.uuid()) == bytes:
                            print("bytes")
                        else:
                            print("Caracteristic in hex")
                            print("-----")
                            print("Char target ==>" )
                            print(arr[position[0]][3])
                            print("-----")
                            if char.uuid() == arr[position[0]][3]:
                                if (char.properties() & Bluetooth.PROP_READ ):
                            #print('char {} value = {}'.format(char.uuid(), char.read()))
                                    msg=char.read()
                            #send tuple or prediction result after extraction
                                    print ("Sending to Lora =>")
                                    print (msg)
                                    s.setblocking(True)
                                    s.send(msg)
                                else:
                                    print("Cant read")
                except:
                    continue
        print("desconnecting")
        conn.disconnect()
        bt.deinit()
        print("reinit scanning")
        bt.init()
        bt.start_scan(-1)
    else:
        time.sleep(0.250)
