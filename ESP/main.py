from machine import Pin
import machine
import read as read
import ubinascii
import ws as WS


def do_connect():
    """
    do_connect zorgt ervoor dat de reader verbind met de lokale wifi. Daarnaast gaat op het "caca1300" model een lichtje aan zodra er een wifi verbinding is opgezet.
    """
    global wlan
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('connecting to network...')
    wlan.connect('H369ABEE905', '9C43DECA7AAA')
    print('network config:', wlan.ifconfig())
    while not wlan.isconnected():
        machine.idle()  # save power while waiting
    if wlan.isconnected():
        print("ONLINE!")
        read.do_read()


if __name__ == "__main__":
    do_connect()

