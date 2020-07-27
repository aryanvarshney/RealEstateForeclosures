import flask
from flask import request
import requests
from bs4 import BeautifulSoup
import numpy as np
import smtplib
import time
from datetime import datetime
import csv
import json
import os
from pathlib import Path

app = flask.Flask(__name__)
app.config['DEBUG'] = True

states = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 
    'delaware', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa',
    'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan',
    'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'newhampshire',
    'newjersey', 'newmexico', 'newyork', 'northcarolina', 'northdakota', 'ohio', 'oklahoma',
    'oregon', 'pennsylvania', 'rhodeisland', 'southcarolina', 'southdakota',
    'tennessee', 'texas', 'utah', 'vermont', 'vriginia', 'washington', 'westvirginia',
    'wisconsin', 'wyoming']

db_path = os.path.abspath(os.path.dirname(__file__)) + "/../data/properties.csv"

# Introduction to Real Estate foreclosure leads

# Gets all of the banks that leads are being pulled from Get / -> getAll, Get /{id}, Post / -> add a bank, Put /{id}, Del /{id} 
# Get /search?name=x
@app.route('/rsforeclosure/bank/', methods=['GET'])
def bank():
    return "Currently only servicing Bank of America (boa)"


# Posts all the new listings from Bank of America Post /bank/{name}/listings
@app.route('/bank/<bank_name>/properties', methods=['POST'])
def add_new_listings(bank_name):
    if (bank_name != 'boa'):
        flask.abort(404, "Please enter a valid bank")
    curr_links = get_db()
    currList = []
    old_links = [d['sourcelink'] for d in curr_links]
    for i in states:
        URL = 'https://foreclosures.bankofamerica.com/search/' + i
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.findAll('div', {'class':'rec-result'})
        for link in links:
            address = link['data-location']
            link_string = link.findChild().findChild().findChild()['href']
            new_link = 'foreclosures.bankofamerica.com' + link_string
            if new_link not in old_links:
                new_listing = {'sourcelink':new_link, 'location':address, 'state':i, 'datetime':datetime.now()}
                currList.append(new_listing)
                curr_links.append(new_listing)
    post_db(curr_links)
    output_list = [{k: v for k, v in d.items() if k != 'datetime'} for d in currList]
    return json.dumps(output_list)

# Gets all of the properties in the db
@app.route('/properties', methods=['GET'])
def properties():
    curr_links = get_db()
    daysListed = None
    if 'daysListed' in request.args:
        try:
            daysListed = int(request.args['daysListed'])
        except ValueError:
            request_invalid(400, "Please use a valid integer for the number of days listed")
    
    if (daysListed != None):
        output_list = [d for d in curr_links if (datetime.now() - datetime.strptime(d['datetime'], '%Y-%m-%d %H:%M:%S.%f')).days <= (daysListed-1)]
    output_list = [{k: v for k, v in d.items() if k != 'datetime'} for d in output_list]
    return json.dumps(output_list)

# Gets all of the valid states
@app.route('/properties/state/', methods=['GET'])
def get_usstates():
    return json.dumps(states)

# Gets all of the properties in the given state
@app.route('/properties/state/<state_name>', methods=['GET'])
def get_states(state_name):
    if(state_name not in states):
        request_invalid(404, 'The state you input is not part of the valid states. Use the /properties/state to see valid entries')
    else:
        daysListed = None
        if 'daysListed' in request.args:
            try:
                daysListed = int(request.args['daysListed'])
            except ValueError:
                request_invalid(400, "Please use a valid integer for the number of days listed")
        curr_links = get_db()
        output_list = [d for d in curr_links if d['state'] == state_name]
        if (daysListed != None):
            output_list = [d for d in output_list if (datetime.now() - datetime.strptime(d['datetime'], '%Y-%m-%d %H:%M:%S.%f')).days <= (daysListed-1)]
        return json.dumps(output_list)


# Gets information about day-based filtering
@app.route('/properties/days/', methods=['GET'])
def get_dates():
    return "Add the number of days listed to filter to those properties"

# Gets property list for specified number of days or less
@app.route('/properties/days/<number>')
def get_listings_by_time(number):
    try:
        days = int(number)
    except ValueError:
        request_invalid(400, 'Use a valid integer to represent number of days')
    curr_links = get_db()
    output_list = [d for d in curr_links if (datetime.now() - datetime.strptime(d['datetime'], '%Y-%m-%d %H:%M:%S.%f')).days <= (days-1)]
    return json.dumps(output_list)

# Reroutes all bad requests with respective error code and message
@app.route('/invalid')
def request_invalid(code, msg):
    flask.abort(code, msg)

# Returns a list of dictionaries version of database
def get_db():
    with open(db_path) as f:
        curr_links = [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]
    return curr_links

# Updates the database with the current data
def post_db(curr_links):
    keys = curr_links[0].keys()
    with open(db_path, 'w') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(curr_links)

app.run()