import flask

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


if __name__ == '__main__':
    app.run(debug=True)
