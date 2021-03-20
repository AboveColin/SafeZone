from time import sleep_ms
from machine import Pin, SPI
from mfrc522 import MFRC522
import urequests
import machine
import ubinascii

api_host = "http://URL/"

D_ID = ubinascii.hexlify(machine.unique_id()).decode('utf-8')

## Colin's Configuratie
if D_ID == "9c9c1fc88ea8":
    ledG = Pin(32, Pin.OUT)
    ledR = Pin(33, Pin.OUT)

    sck = Pin(18, Pin.OUT)
    mosi = Pin(23, Pin.OUT)
    miso = Pin(19, Pin.OUT)
    spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

    sda = Pin(21, Pin.OUT)

if D_ID == "caca1300":
    sck = Pin(14, Pin.OUT)
    mosi = Pin(13, Pin.OUT)
    miso = Pin(12, Pin.OUT)
    spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

    sda = Pin(15, Pin.OUT)


def send_online():
    """
    Stuurt een request naar de server/hub met het ID van de hardware.
    Hiermee weet de server dat de reader online is gekomen.
    """
    data = [{"esp_id": D_ID}]
    try:
        urequests.request("GET", api_host+"online", json=data,
                          headers={'content-type': 'application/json'})
    except:
        # Backup server?
        print("error?")


def online_check():
    """
    Stuurt een request/ping naar de server/hub met het ID van de hardware.
    Hierdoor weet de server dat de reader nogsteeds online is.
    """
    data = [{"esp_id": D_ID}]
    try:
        urequests.request("GET", api_host+"online_check", json=data,
                          headers={'content-type': 'application/json'})
    except:
        # Backup server?
        print("error?")


def do_read():
    """
    Deze functie wacht voor een langskomende tag. Zodra een tag wordt gescanned, wordt deze informatie doorgestuurd naar: "http://192.168.2.38:5000/hit".
    Daarnaast gaat er een groen lampje aan zodra een goede tag wordt gelezen.
    """
    if D_ID == "9c9c1fc88ea8":
        ledR.value(1)
    c = 0
    try:
        while True:
            if c == 5:
                online_check()
                c = 0
            else:
                c += 1

            rdr = MFRC522(spi, sda)
            (stat, tag_type) = rdr.request(rdr.REQIDL)

            if stat == rdr.OK:

                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:
                    uid = raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid	 : 0x%02x%02x%02x%02x" % (uid))
                    print("")

                    if rdr.select_tag(raw_uid) == rdr.OK:

                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                            print("Address 8 data: %s" % rdr.read(8))

                            data = [{"tag_id": str(rdr.read(8)), "esp_id": D_ID}]
                            try:
                                urequests.request("GET", api_host+"hit", json=data, headers = {'content-type': 'application/json'})
                            except:
                                print("error?")

                            online_check()

                            rdr.stop_crypto1()
                            if D_ID == "9c9c1fc88ea8":
                                ledR.value(0)
                                ledG.value(1)
                            sleep_ms(1000)
                            if D_ID == "9c9c1fc88ea8":
                                ledR.value(1)
                                ledG.value(0)
                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")

    except KeyboardInterrupt:
        if D_ID == "9c9c1fc88ea8":
            ledR.value(0)
            ledG.value(1)
        print("Bye")




