import socket
from machine import Pin
import machine
import ubinascii
from time import sleep_ms

D_ID = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
if D_ID == "9c9c1fc88ea8":
    ledG = Pin(32, Pin.OUT)
    ledR = Pin(33, Pin.OUT)
    ledW = Pin(2, Pin.OUT)
    ledW.value(0)

if D_ID == "caca1300":
    ledW = Pin(16, Pin.OUT)
    ledW.value(1)



def connect():
    global s
    HOST = "192.168.2.28"
    PORT = 4000
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
        s.connect((HOST, PORT))
        print('Connection made')
    except Exception as e:
        print(e)
        sleep_ms(4000)
        connect()
    return s


def send_message(msg, s):
    s.send(bytes(str(msg), "utf-8"))


def receive_message(s):
    try:
        data = s.recv(1024)
        message = data.decode("utf-8")
        if message == "READ_SUCCESSFUL":
            if D_ID == "9c9c1fc88ea8":
                ledR.value(0)
                ledG.value(1)
                sleep_ms(1000)
                ledR.value(1)
                ledG.value(0)
    except Exception as e:
        print(e)


def disconnect():
    s.close()
