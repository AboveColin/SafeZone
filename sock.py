#!/usr/bin/python
import socket
import threading
import requests
import json
from SafeZone.models import log
from SafeZone.logs import logger
import urllib3
urllib3.disable_warnings()

def process_data(data, clientsocket, addr):
    """Deze functie verwerkt alle binnenkomende data en zet door naar de goede API call/endpoint
    Parameters:
     - Cliensocket: huidige socket, waarmee de ESP is verbonden.
     - Addr: IP addr van de ESP
     - Data: Binnengekomen JSON.
    """
    try:
        type = data[0]['type']
        
        if type == 'read':
            requests.get("https://127.0.0.1:5000/api/hit", json=data, headers = {'content-type': 'application/json'}, verify=False)
            
            command = "READ_SUCCESSFUL"
            clientsocket.send(command.encode("utf-8"))
            logger.info(str(log('{}').log_prefix_addr() + ' Commando {} gestuurd naar reader').format(addr, command))
            
        
        elif type == 'online':
            requests.get("https://127.0.0.1:5000/api/online", json=data, headers = {'content-type': 'application/json'}, verify=False)
            
            command = "SOCKET_CONNECTED"
            clientsocket.send(command.encode("utf-8"))
            logger.info(str(log('{}').log_prefix_addr() + ' Commando {} gestuurd naar reader').format(addr, command))
            
        
        elif type == 'online_check':
            requests.get("https://127.0.0.1:5000/api/online_check", json=data, headers = {'content-type': 'application/json'}, verify=False)
    
    except Exception as e:
        logger.warning(e)


def on_new_client(clientsocket, addr):
    """Wanneer er een nieuwe ESP connect dan wordt deze functie gestart, om alle binnenkomende berichten op te vangen.
    Parameters:
     - Cliensocket: huidige socket, waarmee de ESP is verbonden.
     - Addr: IP addr van de ESP
    """
    while True:
        try:
        
            msg = clientsocket.recv(1024)
            
            logger.info(str(log('{}').log_prefix_addr() + ' {}').format(addr[0], msg))
            
            data = str(msg)
            data = json.loads(data.replace("'", '"').replace('b"',"")[:-1])
            process_data(data, clientsocket, addr[0])


        except Exception:
            clientsocket.close()
    clientsocket.close()


def main():
    """Deze functie start de socket en laat het wachten op binnenkomende verbindingen, zodra er een verbinding binnenkomt geeft ie het een aparte Thread en stuurt ie het door naar functie 'on_new_client'
    """
    HOST = "192.168.2.28"
    PORT = 4000

    s = socket.socket()
    s.bind((HOST, PORT))
    logger.info("Socket ingeschakeld, wachten voor binnenkomende verbindingen....")
    s.listen()
    

    while True:
        try:
            c, addr = s.accept()
            new_inst = threading.Thread(target=on_new_client, args=(c,addr))
            new_inst.daemon = True
            new_inst.start()
        
        except Exception as e:
            logger.warning(e)

    s.close()

if __name__ == "__main__":
    main()
