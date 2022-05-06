#################################################
# LoRa receiver
#
# Jorge Navarro-Ortiz (jorgenavarro@ugr.es), 2021
#################################################

DEBUG=False

from network import LoRa
import socket
import machine
import time

print('\n(c) Fernando Tejero\n')

# initialise LoRa in LORA mode
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
# more params can also be given, like frequency, tx power and spreading factor
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, frequency=868100000, tx_power=3, bandwidth=LoRa.BW_500KHZ, sf=7, preamble=8, coding_rate=LoRa.CODING_4_5)

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Change frequency, spreading factor, coding rate... at any time
lora.frequency(868100000)
lora.sf(7)
lora.coding_rate(LoRa.CODING_4_5)

print('LoRa initialized!')
print('Recibiendo numero de paquetes:')
s.setblocking(True)
iteraciones = s.recv(256)
print('...')
print('Numero de iteraciones: '+ str(iteraciones))

imagen = []
iteraciones = 0
datos = 0
i=0
while i!=iteraciones:
    i=i+1
    # send some data
#    s.setblocking(True)
#    s.send('Hello')

    # get any data received...
    s.setblocking(True)
    print('Paquete numero '+ str(i))
    datos = s.recv(256)
    imagen = imagen+datos
    # if DEBUG:
    #     print('[' + str(i) + '] Message sent: ' + str(message))
    #     print('[' + str(i) + '] LoRa stats: ' + str(lora.stats()))
    print('Mensaje recibido:' + str(datos))

    # if i==1:
    #     time_start=time.ticks_us()
    #
    # if i%packets_per_measurement == 0:
    #     time_end=time.ticks_us()
    #     time_diff=time.ticks_diff(time_end,time_start)
    #     print('[' + str(i) + '] Received ' + str(packets_per_measurement) + ' packets of ' + str(len(message)) + ' bytes in ' + str(time_diff/1e6) + " seconds")
    #     throughput=packets_per_measurement*8*len(message)*1e6/time_diff
    #     print('[' + str(i) + '] Throughput ' + str(throughput) + ' bps')
    #     time_start=time_end

    # wait a random amount of time
#    time.sleep(machine.rng() & 0x0F)
