import requests
from bs4 import BeautifulSoup
import numpy as np
import smtplib
import time
from datetime import datetime

# Contains previous list of houses
curr_links = []

# List of all 50 states
states = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 
    'delaware', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa',
    'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan',
    'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'newhampshire',
    'newjersey', 'newmexico', 'newyork', 'northcarolina', 'northdakota', 'ohio', 'oklahoma',
    'oregon', 'pennsylvania', 'rhodeisland', 'southcarolina', 'southdakota',
    'tennessee', 'texas', 'utah', 'vermont', 'vriginia', 'washington', 'westvirginia',
    'wisconsin', 'wyoming']

# Scrapes Craigslist 
def get_links():
    currList = []
    for state in states:
        URL = 'https://foreclosures.bankofamerica.com/search/' + state
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.findAll('div', {'class':'rec-result'})
        for link in links:
            address = link['data-location']
            link_string = link.findChild().findChild().findChild()['href']
            if link_string not in curr_links:
                currList.append({'sourcelink':('foreclosures.bankofamerica.com' + link_string), 'location':address, 'state':state, 'datetime':datetime.now()})
                curr_links.append(link_string)
    return currList

def send_email(list_to_send, day):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    f=open("RElog.txt", "a+")

    # Try to log in to server and send email
    try:
        server.login('foreclosureleads.noreply@gmail.com', 'foreclosure123')
        # Send email here
        subject = "Foreclosure Listings"
        if(len(list_to_send) == 0):
            body = "There are no new listings"
        else:
            body = "New Listings from BoA \n"
            for link in list_to_send:
                body = body + "\n" + link['location'] + ': ' + link['link'] + ' '

        msg = "Subject: {}\n\n{}".format(subject, body)
        server.sendmail('foreclosureleads.noreply@gmail.com',
            ['foreclosureleads.noreply@gmail.com', 'cultrealestate@gmail.com'], msg)
    except Exception as e:
        # Print any error messages to stdout
        error_message = "Something went wrong on day " + str(day) + str(e) + " \n"
        f.write(error_message)
        print(e)
    finally:
        success_message = "Everything is working as of day " + str(day) + " \n"
        f.write(success_message)
        server.quit()

def main():
    day = 1
    while True:
        t = time.time()
        send_email(get_links(), day)
        time.sleep(86400 - (time.time() - t))
        day = day + 1

if __name__ == "__main__":
    main()