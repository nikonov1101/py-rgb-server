"""
    Index controllers:
    1. Render site index page
"""
from flask import Blueprint, render_template

# Define the blueprint: 'index'
index = Blueprint('index', __name__, url_prefix='/')

# Set the route and accepted methods
@index.route('/', methods=['GET'])
def show_index():
    """ just render index page template """
    return render_template("index/index.html")
