#this program will connect to google's search engine and search for a topic

import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import requests

# Load variables from .env file
load_dotenv()

def searchItem(topic):

    base_url = "https://api.scaleserp.com/search?api_key="
    # Access the API_KEY variable
    api_key = os.getenv("API_KEY")
    print(api_key)
    # Add the API_KEY to the base_url
    url = base_url + api_key
    # Add the topic to the url
    url = url + "&q=" + topic

    # Make the request
    response = requests.get(url)

    #now we need to parse the response for all of the links
    #first we need to convert the response to a json object
    response = response.json()

    #now we need to parse the json object for the links
    #we will store the links in a list
    links = []
    for i in range(len(response['organic_results'])):
        links.append(response['organic_results'][i]['link'])

    #now we need to print the links
    for i in range(len(links)):
        print(links[i])

    return links




searchItem("python")
