from flask import Blueprint, request, jsonify, render_template

from . import serial

# Define the blueprint: 'index'
index = Blueprint('index', __name__, url_prefix='/')


@index.route('/')
def index_page():
    return render_template('index/index.html')


@index.route('get', )
def get_color():
    return jsonify(colors=serial.get_rgb())


@index.route('set', methods=['GET', ])
def set_color():
    red = request.args.get('r', '0')
    green = request.args.get('g', '0')
    blue = request.args.get('b', '0')

    serial.set_rgb(red, green, blue)
    return jsonify(colors=serial.get_rgb())
