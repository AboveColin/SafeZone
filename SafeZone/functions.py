#!/usr/bin/python
from datetime import datetime, timedelta
import SafeZone.db as DB

def get_current_timestamp():
    """Returns the current timestamp"""
    ct = datetime.now()
    ts = ct.timestamp() 
    return ts


def get_data():
    """Verkrijgt alle nodige informatie voor op de dashboard
    """
    data = []
    clients = DB.get_all_clients()
    readers = DB.get_all_readers()

    client_list = []
    admin_reader_list = []

    for reader in readers:
        r_id = reader[0]
        r_last_seen = \
            datetime.fromtimestamp(float(reader[1])).strftime('%d/%m/%Y %H:%M:%S').split('.')
        if datetime.fromtimestamp(float(reader[1])) > datetime.now() - timedelta(seconds=10):
            onoff = 'online'
        else:
            onoff = 'offline'
        admin_reader_list.append([r_id, r_last_seen[0], onoff])

    for client in clients:
        c_data = DB.get_last_hit(client[2])
        c_last_seen = datetime.fromtimestamp(float(c_data[0]))
        c_last_seen = c_last_seen.strftime('%d/%m/%Y %H:%M:%S').split('.')

        client_list.append([client[0], client[1], c_last_seen[0],
                           c_data[1]])

    data.append([admin_reader_list, client_list])

    return data
