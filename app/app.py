import flask

app = flask.Flask(__name__)


@app.route('/')
def index():
    sample_dict = {'message': 'Hello, this is my app!', 'author': 'Agata'}
    return sample_dict


if __name__ == '__main__':
    app.run(debug=True)
