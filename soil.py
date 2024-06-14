#soil misture

import spidev, time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 100000


def soilread(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_value = ((r[1] & 3) << 8) + r[2]
    if(adc_value!=0):
        return converParcent(adc_value)
    else:
        soilread(channel)

def converParcent(data):
    return 100.0 - round(((data * 100) / float(1023)), 1)
