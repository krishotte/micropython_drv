from machine import Pin, SPI
import ustruct as struct
import utime as time


ctrl_pin1 = Pin(22, Pin.OUT, value=1)
# hspi = SPI(1, 10000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
hspi = SPI(2, 1000000, sck=Pin(19), mosi=Pin(23), miso=Pin(18), firstbit=SPI.MSB, phase=1)


def read_bytes():
    """
    reads raw bytes from sensor over the SPI bus
    :return: bytes string - 2 bytes
    """
    ctrl_pin1.value(0)
    time.sleep_ms(2)
    ctrl_pin1.value(1)
    time.sleep_ms(220)
    ctrl_pin1.value(0)
    temp = hspi.read(2)
    ctrl_pin1.value(1)
    return temp


def read_bits():
    """
    diagnostic function
    :return:
    """
    bytes_ = read_bytes()
    int_ = struct.unpack('>H', bytes_)[0]
    bits_ = '{0:016b}'.format(int_)
    print('bytes: ', bytes_, ' bits: ', bits_)
    print('sensor connected: ', '{0:016b}'.format(int_ & 0x04), 'raw value: ', '{0:016b}'.format(int_ >> 3))
    print('celsius: ', (int_ >> 3) * 0.25)
    return bits_


def read_temp():
    """
    reads temperature in deg celsius
    :return: temperature in deg celsius
    """
    bytes_ = read_bytes()
    int_ = struct.unpack('>H', bytes_)[0]
    temp_celsius = (int_ >> 3) * 0.25
    return temp_celsius


def read_bits_c():
    """
    infinite diagnostic read cycle
    :return:
    """
    while True:
        read_bits()
        time.sleep(1)
