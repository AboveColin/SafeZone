from time import sleep_ms
from machine import Pin, SPI
from mfrc522 import MFRC522
import machine
import ubinascii
import ws as WS

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
    ledW = Pin(2, Pin.OUT)
    ledW.value(0)

if D_ID == "caca1300":
    sck = Pin(14, Pin.OUT)
    mosi = Pin(13, Pin.OUT)
    miso = Pin(12, Pin.OUT)
    spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

    sda = Pin(15, Pin.OUT)
    ledW = Pin(16, Pin.OUT)
    ledW.value(1)


def send_online(s):
    """
    Stuurt een request naar de server/hub met het ID van de hardware.
    Hiermee weet de server dat de reader online is gekomen.
    """
    data = [{"type": "online", "esp_id": D_ID}]
    try:
        WS.send_message(str(data), s)
        try:
            data = s.recv(1024)
            message = data.decode("utf-8")
            if message == "SOCKET_CONNECTED":
                if D_ID == "caca1300":
                    ledW.value(0)
                if D_ID == "9c9c1fc88ea8":
                    ledW.value(1)
        except Exception as e:
            print(e)
    except Exception as e:
        # Backup server?
        print(e)


def online_check(s):
    """
    Stuurt een request/ping naar de server/hub met het ID van de hardware.
    Hierdoor weet de server dat de reader nogsteeds online is.
    """
    data = [{"type": "online_check", "esp_id": D_ID}]
    try:
        WS.send_message(str(data), s)
    except Exception as e:
        # Backup server?
        print(e)


def do_read():
    """
    Deze functie wacht voor een langskomende tag. Zodra een tag wordt gescanned, wordt deze informatie doorgestuurd naar: "http://192.168.2.38:5000/hit".
    Daarnaast gaat er een groen lampje aan zodra een goede tag wordt gelezen.
    """

    conne = WS.connect()
    send_online(conne)
    sleep_ms(1000)

    if D_ID == "9c9c1fc88ea8":
        ledR.value(1)
        ledG.value(0)
    c = 0
    try:
        while True:
            if c == 3:
                online_check(conne)
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

                            data = [{"type": "read", "tag_id": str(rdr.read(8)), "esp_id": D_ID}]
                            WS.send_message(str(data), conne)
                            WS.receive_message(conne)

                            online_check(conne)

                            rdr.stop_crypto1()
                            sleep_ms(1000)

                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")

    except KeyboardInterrupt:
        if D_ID == "9c9c1fc88ea8":
            ledR.value(0)
            ledG.value(1)
        print("Bye")
