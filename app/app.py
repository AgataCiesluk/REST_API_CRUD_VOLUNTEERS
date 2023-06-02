import flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

from database.db_config import DB_CONNECTION_ARGS
from database.db_handler import create_connection, get_all_volunteers

app = flask.Flask(__name__)


@app.route('/')
def index():
    sample_dict = {'message': 'Hello, this is my app!', 'author': 'Agata Ciesluk'}
    return sample_dict


@app.route('/volunteers')
def read_all_volunteers():
    all_volunteers = get_all_volunteers(create_connection(*DB_CONNECTION_ARGS))
    return {'volunteers': all_volunteers}


db = SQLAlchemy(app)
from models import Volunteer

@app.route('/volunteers/add')
def add_volunteer():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    phone_number = request.args.get('phone_number')
    vol = Volunteer(first_name, last_name, phone_number)
    print(vol.first_name)
    # volunteer = [first_name, last_name, phone_number]
    # insert_data_into_volunteers_table(volunteer)
    return {'message': 'Volunteer added to DB',
            'volunteer': {'first_name': first_name, 'last_name': last_name, 'phone_number': phone_number}}

# @app.route('/volunteers/delete')


if __name__ == '__main__':
    app.run(debug=True)
