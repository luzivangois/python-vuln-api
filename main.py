from flask import Flask

app = Flask(__name__)

@app.route('/teste', methods=['GET', 'POST'])
def teste():
    return ("teste")

app.run()