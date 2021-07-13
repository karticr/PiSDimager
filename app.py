from flask import Flask, Response, redirect, url_for, request, session, abort, render_template
from threading import Thread

from libs.shellController import ShellController
from libs.configController import ConfigController

from routes.home_page import home_page

sc   = ShellController()
conf = ConfigController()


app = Flask(__name__)
app.register_blueprint(home_page)

app.conf = conf
app.sc   = sc


@app.route('/yolo')
def somehandler():
    return "hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = True) 