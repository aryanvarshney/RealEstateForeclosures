# Real Estate foreclosure leads
Created by Aryan Varshney

This project is meant to pull foreclosure leads from all of the US banks and compile into one, easy to use, platform and emailing service.

There are two main functions for this project:

 1. Pull foreclosure listings from bank websites and store the data
 2. Filter the data obtained to get foreclosure listings with the client's specifications and provide an automated email service

## Project Structure
```
+-- script.py
+-- api
|   webapp.py
+-- _data
|   +-- properties.csv
+-- logs
|   +-- RElog.txt
+-- test
```

## Setup

Important Python packages to install/import:
1. Flask for local web server
2. BeautifulSoup for webscraping
3. Smtplib for email services

To start the web server and use the APIs, run the webapp.py file using ```python webapp.py```

## Usage

### Email Service
For the automated email service, simply run ```python script.py```

### API endpoints

**Fetching currently serviced banks**  
Request Format: /bank/  
Request Type: GET  
Returned Data Format: plain/text  
Description: This endpoint returns the names of the banks and their symbol where data can currently be scraped from.  
Example/Current output:  
```Currently only servicing Bank of America(boa)```


**Scraping specific bank foreclosure listings**  
Request Format: /bank/<bank_symbol>/properties  
Request Type: POST  
Returned Data Format: JSON  
Description: This endpoint scrapes the given banks foreclosure listings and adds all the new listings since the previous call. The new listings that were updated into the database are also returned in JSON format  
Example Output:  
```
[{"sourcelink":"foreclosures.bankofamerica.com/property-details/01106542", "location": "CA-Sacramento-95828", "state": "california", "datetime": "2020-07-26 10:00:57.209186"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106473","location": "CA-Lodi-95242","state": "california","datetime": "2020-07-26 10:00:57.209223"}]
```


**Get all foreclosure listings in the database**  
Request Format: /properties  
Request Type: GET  
Returned Data Format: JSON  
Description: Returns all of the property listings in the database along with their date added, state, and Zip Code  
Request Parameters:  
 - daysListed (optional): Specifies the maximum number of days listed on the market  
Example Request: /properties?daysListed=2  
Example Output:  
```
[{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106496", "location": "AZ-Buckeye-85326", "state": "arizona"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106314", "location": "AR-Augusta-72006", "state": "arkansas"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106542", "location": "CA-Sacramento-95828", "state": "california"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106473", "location": "CA-Lodi-95242", "state": "california"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106216", "location": "FL-Miami-33172", "state": "florida"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01105748", "location": "FL-Port St Lucie-34983", "state": "florida"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106402", "location": "FL-Tamarac-33321", "state": "florida"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01105573", "location": "FL-Boynton Beach-33437", "state": "florida"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106497", "location": "FL-Palm Bay-32905", "state": "florida"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106218", "location": "FL-Boynton Beach-33437", "state": "florida"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106550", "location": "IL-Plainfield-60544", "state": "illinois"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106576", "location": "IL-Lockport-60441", "state": "illinois"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01103948", "location": "IL-Chicago-60629", "state": "illinois"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106474", "location": "MD-Glen Burnie-21060", "state": "maryland"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106397", "location": "MA-Ashby-01431", "state": "massachusetts"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01102044", "location": "NV-Las Vegas-89129", "state": "nevada"},
{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106259", "location": "OH-Glouster-45732", "state": "ohio"}]
```


**Get all currently serviced states**  
Request Format: /properties/state/  
Request type: GET  
Returned Data Format: List (JSON)  
Description: Returns the currently serviced states as their request name format (Reference following endpoint)  
Example/Current Output:  
```
["alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi", "missouri", "montana", "nebraska", "nevada", "newhampshire", "newjersey", "newmexico", "newyork", "northcarolina", "northdakota", "ohio", "oklahoma", "oregon", "pennsylvania", "rhodeisland", "southcarolina", "southdakota", "tennessee", "texas", "utah", "vermont", "vriginia", "washington", "westvirginia", "wisconsin", "wyoming"]
```

**Get all property listings in a state**  
Request Format: /properties/state/<state_name>  
Request type: GET  
Returned Data Format: JSON  
Description: Returns all property listings from the specified state. Invalid requests are met with a 400 "Please enter a valid state name" response  
Request Parameters:  
 - daysListed (optional): Specifies the maximum number of days listed on the market  

Example Request: /properties/state/arizona  
Example Output:  
```
[{"sourcelink": "foreclosures.bankofamerica.com/property-details/01106496", "location": "AZ-Buckeye-85326", "state": "arizona", "datetime": "2020-07-26 10:00:56.275607"}]
```