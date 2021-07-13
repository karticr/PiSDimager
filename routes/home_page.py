from flask import Blueprint, render_template, Response, redirect, url_for, request,jsonify
from flask import current_app as app
from threading import Thread
home_page = Blueprint('home_page',__name__)

@home_page.route('/')
def home():
    sd_cards = app.sc.USBDeviceList()
    conf     = app.conf.loadConfigFromFile()

    return render_template('home_page/home_page.html', conf=conf, sd_card_list=sd_cards)

@home_page.route('/test')
def testRun():
    Thread(target=app.sc.ImageProcessor, args=('/dev/sdg', "test.img")).start()
    return "okay"