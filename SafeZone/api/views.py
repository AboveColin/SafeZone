
from flask import Flask, Blueprint, render_template, request, jsonify, request
import SafeZone.functions as Function
import json
import logging
from SafeZone.models import log, log_type
from SafeZone.logs import logger

api_blueprint = Blueprint('api',
                              __name__,
                              template_folder='templates/')

online_list = []

@api_blueprint.route('/online')
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


@api_blueprint.route('/online_check')
def online_check():
    request_data = json.loads(request.data)
    reader_id = request_data[0]['esp_id']

    ts = Function.get_current_timestamp()

    if reader_id not in online_list:
        online_list.append(reader_id)

    Function.DB.update_reader_last_seen(reader_id, ts)

    logger.info(log(reader_id).log_prefix_r() + ' ' + log_type.PING + ' Ping')
    return ''


@api_blueprint.route('/hit')
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


@api_blueprint.route('/get_data')
def return_data():
    data = Function.get_data()

    return jsonify(data[0])