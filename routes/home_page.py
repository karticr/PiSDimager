from flask import Blueprint, render_template, Response, redirect, url_for, request,jsonify
from flask import current_app as app

home_page = Blueprint('home_page',__name__)

@home_page.route('/')
def home():
    return "homepage"