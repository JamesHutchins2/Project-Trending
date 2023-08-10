#we will loop through all of the links from the called script, and go to each one, and scrape all of the content from the page
import requests
from bs4 import BeautifulSoup
from langdetect import detect

def collectPages():

    #call the google searches connection

    #for now we will just use a list of links

    links =  [

             "https://www.python.org/",
             "https://www.html.it/guide/guida-python/",
             "https://it.wikipedia.org/wiki/Python",
             "https://www.python.it/",
             "https://www.programmareinpython.it/",
             "https://aws.amazon.com/it/what-is/python/",
             "https://www.geekandjob.com/wiki/python"

             ]
    for link in links:
        # Send a GET request to the URL
        response = requests.get(link)
        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract the text data from the HTML
        text_data = soup.get_text()
        # Detect the language of the text
        detected_lang = detect(text_data)
        # Check if the detected language is English
        if detected_lang != 'en':
            print(f"Skipped {link} - Detected language: {detected_lang}")
            continue
        # Print the scraped text
        print(text_data)
        print('---' * 20)  # Separator for each link

    #now we will loop through the links and scrape the content from each page
collectPages()