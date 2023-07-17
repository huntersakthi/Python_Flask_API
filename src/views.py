import requests
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import json


views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
#@login_required decorator to check whether the user is logged in before Homepage is displayed 
@login_required
def home():
    if request.method == 'POST':

        #Getting the currency pair which has been provided by the user in the homepage
        pair = request.form.get('pair')

        #Passing the data to get_data method which returns a response
        response = get_data("query",pair)  

        #Sending the response to be displayed 
        return (response._content)
    
    #HTMl page to be displayed for Homepage
    return render_template('home.html',user = current_user)

@views.route('/summary')
@login_required
def summary():

     #Passing the summary string to get_data method which returns overall market summary
    response = get_data("summary",None) 

    #Sending the response to be displayed   
    return (response._content)

#Method to check the request type and make a API request
def get_data(type,pair):

    try:
        #Open the config file which has the API
        with open("src\config\config.json","r") as f:
            config = json.load(f)
        if type == 'summary':    
            url = config[type]["url"]
        else:
            temp = config[type]["url"]

            #Concatenating the api with the user provided input cryptocurrency pair
            url = temp+pair +'/summary'

        #Making an API call to ge tthe data
        response = requests.get(url)

        return response
    
    except:
        print('File Not Found')
