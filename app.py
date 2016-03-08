import os

from flask import Flask


################################### CONFIG #####################################
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


################################### ROUTES #####################################
@app.route('/')
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
