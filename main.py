from flask import Flask, request

from user import User

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = True


@app.route('/', methods=['POST'])
def hello():
    id = request.form['id']
    eta1 = request.form['eta1']
    eta2 = request.form['eta2']
    type = request.form['type']
    user = User(id, eta1, eta2, type)
    return id


if __name__ == "__main__":
    app.run()
