import logging
import sys

import flask
from flask import request, jsonify

from database.db_config import DB_CONNECTION_PARAMS
from database.db_handler import db_add_volunteer, db_delete_volunteer, get_volunteer_by_id, get_all_volunteers, \
    db_update_volunteer
from exceptions import NoRecordFound
from models import db

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
    try:
        volunteer = db_update_volunteer(id, db,
                                    request.args.get('first_name'),
                                    request.args.get('last_name'),
                                    request.args.get('phone_number'))
    except NoRecordFound:
        return jsonify({'error': f'Record with id={id} not found in DB'}), 404
    return {'message': f'Volunteer {volunteer.first_name} {volunteer.last_name} updated in DB'}


if __name__ == '__main__':
    app.run(debug=True)
