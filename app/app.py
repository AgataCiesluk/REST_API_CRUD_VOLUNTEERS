import flask
from flask import request

from models import db, Volunteer
from database.db_config import DB_CONNECTION_ARGS
from database.db_handler import create_connection, get_all_volunteers, insert_data_into_volunteers_table

app = flask.Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://' \
                                        f'{DB_CONNECTION_ARGS[1]}:' \
                                        f'{DB_CONNECTION_ARGS[2]}@' \
                                        f'{DB_CONNECTION_ARGS[3]}:' \
                                        f'{DB_CONNECTION_ARGS[4]}/' \
                                        f'{DB_CONNECTION_ARGS[0]}'
db.init_app(app)

@app.route('/')
def index():
    sample_dict = {'message': 'Hello, this is my app!', 'author': 'Agata Ciesluk'}
    return sample_dict


@app.route('/volunteers')
def read_all_volunteers():
    all_volunteers = get_all_volunteers(create_connection(*DB_CONNECTION_ARGS))
    return {'volunteers': all_volunteers}

# wyprobowac POST w Postmanie
@app.route('/volunteers/add')
def add_volunteer():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    phone_number = request.args.get('phone_number')
    volunteer = Volunteer(first_name, last_name, phone_number)

    db.session.add(volunteer)
    db.session.commit()
    return {'message': 'Volunteer added to DB',
            'volunteer': {'first_name': volunteer.first_name,
                          'last_name': volunteer.last_name,
                          'phone_number': volunteer.phone_number}}

# @app.route('/volunteers/delete')


if __name__ == '__main__':
    app.run(debug=True)
