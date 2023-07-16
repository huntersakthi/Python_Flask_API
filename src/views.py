import requests
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json


views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        pair = request.form.get('pair')

        response = get_data("query",pair)   
        return (response._content)
    return render_template('home.html',user = current_user)

@views.route('/summary')
@login_required
def summary():

    response = get_data("summary",None)   
    return (response._content)

@views.route('/query', methods=['GET', 'POST'])
@login_required
def market():
    if request.method == 'POST':
        pair = request.form.get('pair')

    response = get_data("query",pair)   
    return (response._content)


def get_data(type,pair):

    try:
        with open("src\config\config.json","r") as f:
            config = json.load(f)
        if type == 'summary':    
            url = config[type]["url"]
        else:
            temp = config[type]["url"]
            url = temp+pair +'/summary'

        # print(url)
        response = requests.get(url)

        return response
    
    except:
        return None
