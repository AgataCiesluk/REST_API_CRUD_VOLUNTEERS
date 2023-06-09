import logging
import sys

import flask
from flask import request, jsonify

from database.db_config import DB_CONNECTION_PARAMS
from database.db_handler import db_add_volunteer, db_delete_volunteer, get_volunteer_by_id, get_all_volunteers
from exceptions import NoRecordFound
from models import db, Volunteer
from utils import models_list_to_dict

logger = logging.getLogger("volunteers_app")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "[%(asctime)s - %(levelname)s] %(funcName)s() - %(message)s")
stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.debug("Hello world")

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://' \
                                        f'{DB_CONNECTION_PARAMS.get("DB_USER")}:' \
                                        f'{DB_CONNECTION_PARAMS.get("DB_PASSWORD")}@' \
                                        f'{DB_CONNECTION_PARAMS.get("DB_HOST")}:' \
                                        f'{DB_CONNECTION_PARAMS.get("DB_PORT")}/' \
                                        f'{DB_CONNECTION_PARAMS.get("DB_NAME")}'
db.init_app(app)


@app.route('/volunteers')
def read_all_volunteers():
    volunteers = get_all_volunteers()
    return {'volunteers': volunteers}


@app.route('/volunteers', methods=['GET', 'POST'])
def add_volunteer():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    phone_number = request.args.get('phone_number')
    volunteer = db_add_volunteer(first_name, last_name, phone_number, db)
    return {'message': 'Volunteer added to DB',
            'volunteer': {'first_name': volunteer.first_name,
                          'last_name': volunteer.last_name,
                          'phone_number': volunteer.phone_number}}


@app.route('/volunteers/delete/<int:id>', methods=['DELETE'])
def delete_volunteer(id):
    try:
        volunteer = db_delete_volunteer(id, db)
    except NoRecordFound:
        return jsonify({'error': f'Record with id={id} not found in DB'}), 404
    except:
        return jsonify({'error': f'Unknown Error during item deletion from DB'}), 500
    else:
        return {'message': f'Volunteer {volunteer.first_name} {volunteer.last_name} deleted from DB'}


@app.route('/volunteers/update/<int:id>', methods=['PUT'])
def update_volunteer(id):
    # volunteer should not be used in app.py - only in db_handler to keep modules isolated.
    try:
        volunteer = get_volunteer_by_id(id)
    except NoRecordFound:
        return jsonify({'error': f'Record with id={id} not found in DB'}), 404
    first_name = request.json['first_name']
    if first_name:  # TO_DO: methods to validate first_name
        volunteer.first_name = first_name
    last_name = request.json['last_name']
    if last_name:  # TO_DO: methods to validate last_name
        volunteer.last_name = last_name
    phone_number = request.json['phone_number']
    if phone_number:  # TO_DO: methods to validate phone_number
        volunteer.phone_number = phone_number
    # TO_DO: method to update Volunteer in DB. Close in try and except error 5XX - sth like UnknownError.
    db.session.flush()
    db.session.commit()
    return {'message': f'Volunteer {volunteer.first_name} {volunteer.last_name} updated in DB'}


if __name__ == '__main__':
    app.run(debug=True)
