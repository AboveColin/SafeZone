from machine import Pin
import machine
import read as read
import ubinascii
import online

D_ID = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
if D_ID == "caca1300":
    ledW = Pin(16, Pin.OUT)
    ledW.value(1)


def do_connect():
    """
    do_connect zorgt ervoor dat de reader verbind met de lokale wifi. Daarnaast gaat op het "caca1300" model een lichtje aan zodra er een wifi verbinding is opgezet.
    """
    global wlan
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('connecting to network...')
    wlan.connect('***', '***')
    print('network config:', wlan.ifconfig())
    while not wlan.isconnected():
        if D_ID == "caca1300":
            ledW.value(1)
        machine.idle()  # save power while waiting
    if wlan.isconnected():
        if D_ID == "caca1300":
            ledW.value(0)
        print("ONLINE!")
        read.send_online()


if __name__ == "__main__":
    do_connect()
    read.do_read()
