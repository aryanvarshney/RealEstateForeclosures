import requests
import numpy as np
import smtplib
import time
import json

# Contains previous list of houses
curr_links = []

# Given a list, sends an email to the necessary addresses
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
                for key, value in link.items():
                    if(key == 'location'):
                        location = value
                    if(key == 'sourcelink'):
                        sourcelink = value
                body = body + "\n" + location + ': ' + sourcelink + ' '

        msg = "Subject: {}\n\n{}".format(subject, body)
        server.sendmail('foreclosureleads.noreply@gmail.com',
            ['foreclosureleads.noreply@gmail.com'], msg)
    except Exception as e:
        # Print any error messages to stdout
        error_message = "Something went wrong on day " + str(day) + str(e) + " \n"
        f.write(error_message)
        print(e)
    finally:
        success_message = "Everything is working as of day " + str(day) + " \n"
        f.write(success_message)
        server.quit()

# Script to send email daily
def main():
    day = 1
    while True:
        t = time.time()
        x = requests.post('127.0.0.1:5000/bank/boa/properties')
        re_list = requests.get('127.0.0.1:5000/properties?daysListed=1')
        send_email(re_list.content, day)
        time.sleep(86400 - (time.time() - t))
        day = day + 1

if __name__ == "__main__":
    main()