""" LoPy LoRaWAN Nano Gateway configuration options """

import machine
import ubinascii

WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()
# Set  the Gateway ID to be the first 3 bytes of MAC address + 'FFFE' + last 3 bytes of MAC address
GATEWAY_ID = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]

#SERVER = '192.168.0.11'
SERVER = '192.168.0.18'
PORT = 1700

NTP = "pool.ntp.org"
NTP_PERIOD_S = 3600

WIFI_SSID = 'myssid'
WIFI_PASS = 'ssidpass'
#WIFI_SSID = 'LP-Core'
#WIFI_PASS = 'OFaquuaCei6eegh'
# for EU868
#LORA_FREQUENCY = 868100000
#LORA_GW_DR = "SF7BW125" # DR_5
#LORA_NODE_DR = 5

#LORA_FREQUENCY = 868100000
#LORA_GW_DR = "SF7BW125" # DR_5
#LORA_NODE_DR = 5

# for US915
#LORA_FREQUENCY = 905300000
#LORA_GW_DR = "SF7BW125" # DR_3
#LORA_NODE_DR = 5

# for EU868
#LORA_FREQUENCY = 903900000
#LORA_GW_DR = "SF7BW125" # DR_3
#LORA_NODE_DR = 3
# for EU868
#LORA_FREQUENCY = 868500000
#LORA_GW_DR = "SF7BW125" # DR_5
#LORA_NODE_DR = 5
LORA_FREQUENCY = 917000000
LORA_GW_DR = "SF7BW125" # DR_5
LORA_NODE_DR = 5
