import pandas as pd
import numpy as np
import os
import re
from bs4 import BeautifulSoup
import http.client
import json

from dotenv import load_dotenv
import requests

# Load variables from .env file
load_dotenv()
api_key = os.getenv("SERPER")

def search(topic, resultCount):

    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": topic
    })

    headers = {
    'X-API-KEY': api_key,
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data.decode("utf-8")


#item = search("amazon",10)

def extract_links(json_obj):
    links = []

    # Extracting from knowledgeGraph
    knowledge_graph = json_obj.get('knowledgeGraph', {})
    links.append(knowledge_graph.get('website'))
    links.append(knowledge_graph.get('descriptionLink'))

    # Extracting from organic and sitelinks
    for item in json_obj.get('organic', []):
        links.append(item.get('link'))
        sitelinks = item.get('sitelinks', [])
        for site in sitelinks:
            links.append(site.get('link'))
    
    # Remove None values and return
    return [link for link in links if link]


item = {"searchParameters":{"q":"amazon","type":"search"},"knowledgeGraph":{"title":"Amazon.com","type":"E-commerce company","website":"http://www.amazon.com/","imageUrl":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxb2j-tkUCOz7eJEnEMstANtQ_NaWycwmTRyINqfjP9WqnpL6JQDYwVys&s=0","description":"Amazon.com, Inc. is an American multinational technology company focusing on e-commerce, cloud computing, online advertising, digital streaming, and artificial intelligence.","descriptionSource":"Wikipedia","descriptionLink":"https://en.wikipedia.org/wiki/Amazon_(company)","attributes":{"CEO":"Andy Jassy (Jul 5, 2021–)","CFO":"Brian T. Olsavsky","Mascot":"Peccy","Founder":"Jeff Bezos","Founded":"July 5, 1994, Bellevue, WA","Revenue":"514 billion USD (2022)","President":"Andy Jassy"}},"organic":[{"title":"Amazon.com","link":"https://www.amazon.com/","snippet":"Free shipping on millions of items. Get the best of Shopping and Entertainment with Prime. Enjoy low prices and great deals on the largest selection of ...","sitelinks":[{"title":"Amazon Prime","link":"https://www.amazon.com/amazonprime"},{"title":"Books","link":"https://www.amazon.com/books-used-books-textbooks/b?ie=UTF8&node=283155"},{"title":"Today's Deals","link":"https://www.amazon.com/gp/goldbox"},{"title":"Prime Video","link":"https://www.amazon.com/Amazon-Video/b?ie=UTF8&node=2858778011"},{"title":"Prime Day 2023","link":"https://www.amazon.com/primeday"},{"title":"Amazon Go is a new kind of ...","link":"https://www.amazon.com/b?ie=UTF8&node=16008589011"}],"position":1},{"title":"Amazon.jobs: Help us build Earth's most customer-centric company.","link":"https://www.amazon.jobs/","snippet":"Search open jobs and learn about job opportunities at Amazon warehouses and stores. View open jobs. Software Development. Explore job opportunities and what ...","sitelinks":[{"title":"Working at Amazon","link":"https://www.amazon.jobs/en/landing_pages/working-at-amazon"},{"title":"Search","link":"https://www.amazon.jobs/en/search"},{"title":"Find Jobs","link":"https://www.amazon.jobs/en-gb"},{"title":"Find jobs by job category","link":"https://www.amazon.jobs/search-jobcategory"}],"imageUrl":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbb-_GA1GVQUcwgbeIjmjvzh76eZq0Xm60LZAvH9v9qCZTD7Le8IQUeIk&s","position":2},{"title":"Amazon (company) - Wikipedia","link":"https://en.wikipedia.org/wiki/Amazon_(company)","snippet":"Amazon.com, Inc. is an American multinational technology company focusing on e-commerce, cloud computing, online advertising, digital streaming, ...","imageUrl":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRrrvuuGoCB9RL2LTHN83UjpK-C_yhg7W98kiB9uM9dAH2q85RrVe7HjMo&s","position":3},{"title":"About Amazon","link":"https://www.aboutamazon.com/","snippet":"News announcements, original stories, and facts about Amazon.","imageUrl":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRbzUSBjYI3zHoUEVlNU8SkDgNAq1hABvtbhjls1TCdgtGb_NBJvZ3TcM&s","position":4},{"title":"Amazon.com | Seattle WA - Facebook","link":"https://facebook.com/Amazon/","snippet":"Amazon.com, Seattle, Washington. 30191833 likes · 93201 talking about this. Official Facebook page of www.amazon.com.","position":5}],"relatedSearches":[{"query":"Amazon jobs login"},{"query":"www.amazon.jobs work from home"},{"query":"Amazon de"},{"query":"Amazon Prime login"},{"query":"Amazon warehouse jobs"},{"query":"Amazon seller"},{"query":"Amazon force"},{"query":"Amazon phone number"}]}
item = extract_links(item)

print(item)


def scrapeSite(link):

    #Send request to the page at the link
    page = requests.get(link)

    # Use BS4 to parse the page
    soup = BeautifulSoup(page.text, 'html.parser')

    # Return the text of the page
    return soup.get_text()


def cleanText(text):

    # Remove all non-alphanumeric characters
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
    
    # Remove all extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Return the cleaned text
    return text
