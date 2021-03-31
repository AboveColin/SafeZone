#!/usr/bin/python
from flask import Flask, render_template, request, jsonify
import functions as Function
import json
import logging
from models import log, log_type
from logs import logger


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

online_list = []


@app.route('/')
def index():
    return 'Active'


@app.route('/online')
def online():
    request_data = json.loads(request.data)
    reader_id = request_data[0]['esp_id']

    ts = Function.get_current_timestamp()

    readers = Function.DB.get_all_readers()
    reader_list = []
    for reader in readers:
        r_id = reader[0]
        reader_list.append(r_id)

    if reader_id not in reader_list:
        Function.DB.submit_reader_to_db(reader_id, ts)
        reader_list.append(reader_id)

    if reader_id not in online_list:
        online_list.append(reader_id)

    logger.info(log(reader_id).log_prefix_r() + ' ' + log_type.ONLINE + ' Reader {} is zojuist online gekomen.'.format(reader_id))
    return ''


@app.route('/online_check')
def online_check():
    request_data = json.loads(request.data)
    reader_id = request_data[0]['esp_id']

    ts = Function.get_current_timestamp()

    if reader_id not in online_list:
        online_list.append(reader_id)

    Function.DB.update_reader_last_seen(reader_id, ts)

    logger.info(log(reader_id).log_prefix_r() + ' ' + log_type.PING + ' Ping')
    return ''


@app.route('/hit')
def hit():
    request_data = json.loads(request.data)

    tag_id = "".join(list(request_data[0]['tag_id'])[-2])
    reader_id = request_data[0]['esp_id']
    ts = Function.get_current_timestamp()

    if reader_id == '9c9c1fc88ea8':

        # START / END

        Function.DB.submit_data_to_db(reader_id, tag_id, ts)

        person = Function.DB.get_person_from_T_id(tag_id)
        
        logger.info(log(reader_id).log_prefix_r() + ' ' + log_type.READ + ' Data ontvangen van Tag: {}'.format(tag_id))
        
        if person is not False:    
            logger.info(log(reader_id).log_prefix_r() + ' ' + log_type.INFO + ' Wandeling client: ' + str(person[0]) + ' gestart.')
       
        else:
            logger.error(log(reader_id).log_prefix_r() + ' ' + log_type.INFO + ' Fout bij het ophalen van data bij gelezen tag')
        
        return reader_id
    
    else:

        Function.DB.submit_data_to_db(reader_id, tag_id, ts)
        logger.info(log(reader_id).log_prefix_r() + ' ' + log_type.READ + ' Data ontvangen van Tag: {}'.format(tag_id))

        return reader_id


@app.route('/admin')
def admin():
    data = Function.get_data()
    return render_template('admin.html',
                           admin_reader_list=data[0][0],
                           clients=data[0][1])


@app.route('/get_data')
def return_data():
    data = Function.get_data()

    return jsonify(data[0])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

    
