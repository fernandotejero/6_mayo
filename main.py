import ov2640
import gc
import time
import sys
from machine import SD
import os
import math
from network import LoRa
import socket
import machine
#import pdb


FNAME = '/sd/test.OV2640_1024x768_JPEG.jpg'#saving to SD card on expansion board
sd = SD()
os.mount(sd, '/sd')

# check the content
print(os.listdir('/sd'))
def main():
    try:
        print("initializing camera")
        #lores: OV2640_320x240_JPEG, OV2640_352x288_JPEG, OV2640_640x480_JPEG
        #hires: OV2640_1024x768_JPEG, OV2640_1280x1024_JPEG, OV2640_1600x1200_JPEG
        #cam = ov2640.ov2640(resolution=ov2640.OV2640_1600x1200_JPEG)
        cam = ov2640.ov2640(resolution=ov2640.OV2640_1024x768_JPEG)
        print(gc.mem_free())

        clen = cam.capture_to_file(FNAME, True)
        print("captured image is %d bytes" % clen)
        print("image is saved to %s" % FNAME)

        #MANDAR DATOS
        DEBUG=False

        print("transmitiendo datos")

        # initialise LoRa in LORA mode
        # Please pick the region that matches where you are using the device:
        # Asia = LoRa.AS923
        # Australia = LoRa.AU915
        # Europe = LoRa.EU868
        # United States = LoRa.US915
        # more params can also be given, like frequency, tx power and spreading factor
        lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, frequency=868100000, tx_power=3, bandwidth=LoRa.BW_500KHZ, sf=6, preamble=8, coding_rate=LoRa.CODING_4_5)

        # create a raw LoRa socket
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # Change frequency, spreading factor, coding rate... at any time
        lora.frequency(868100000)
        lora.sf(6)
        lora.coding_rate(LoRa.CODING_4_5)
        print('LoRa initialized!')

        message = open('/sd/test.OV2640_1024x768_JPEG.jpg')
        message = message.read()
        #tamaño = sys.getsizeof(message)
        tamano = len(message)
        print('tamano:' + str(tamano))
        iteraciones = int(len(message)/150)  #sacamos el numero de iteraciones del bucle while como el tamaño de la imagen/rate maximo
        #message = FNAME/iteraciones
        #pdb.set_trace()
        iteraciones = iteraciones+1
        #para el resto del cociente
        print('iteraciones:' + str(iteraciones))
        numeropaquetes = iteraciones
        s.setblocking(True)
        s.send(int(numeropaquetes))
        contador = 150 #bits por iteracion
        inicio = 0
        final = inicio+contador
        i = 0
        while i!=iteraciones:
            i = i+1
            if True:
                s.setblocking(True)
                s.send(message[inicio:final])
                inicio = inicio+contador
                final = final+contador
                # if DEBUG:
                # print('[' + str(i) + '] Message sent: ' + message)
                # print('[' + str(i) + '] LoRa stats: ' + str(lora.stats()))
            #print('Message: ' + message + str(i))

        # packets_per_measurement=1
        # i=0
        # while True:
        #     i=i+1
        #     # send some data ### LIMITED BY PICOM TO 64 BYTES!!! ###
        #     message = "Hola"
        #     #message='12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345676544' # 221 bytes
        #
        #     if True: #lora.ischannel_free(-100, 1): # additional LBT, RSSI threshold of -100 dBm and timeout of 1 ms
        #         s.setblocking(True)
        #         s.send(message)
        #         if DEBUG:
        #             print('[' + str(i) + '] Message sent: ' + message)
        #             print('[' + str(i) + '] LoRa stats: ' + str(lora.stats()))
        #
        #     if i==1:
        #         time_start=time.ticks_us()
        #
        #     if i%packets_per_measurement == 0:
        #         time_end=time.ticks_us()
        #         time_diff=time.ticks_diff(time_end,time_start)
        #         print('[' + str(i) + '] Sent ' + str(packets_per_measurement) + ' packets of ' + str(len(message)) + ' bytes in ' + str(time_diff/1e6) + " seconds")
        #         throughput=packets_per_measurement*8*len(message)*1e6/time_diff
        #         print('[' + str(i) + '] Throughput ' + str(throughput) + ' bps')
        #         time_start=time_end

            # get any data received...
        #    s.setblocking(False)
        #    data = s.recv(64)
        #    print(data)

            # wait a random amount of time
        #    time.sleep(machine.rng() & 0x0F)

        time.sleep(10)
        try:
            f = open(FNAME, "r")
            #print(f.read())
            exists = True
            print("real")
            f.close()
        except FileNotFoundError:
            exists = False
        sys.exit()

    except KeyboardInterrupt:
        print("exiting...")
        sys.exit()


if __name__ == '__main__':
    main()
