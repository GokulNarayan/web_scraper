# import statements
from bs4 import BeautifulSoup, Comment
import requests
import lxml
import re
from googlesearch import search

# global vars
titles = []
url_names = ['https://www.mckinsey.com/featured-insights/artificial-intelligence/notes-from-the-ai-frontier-modeling-the-impact-of-ai-on-the-world-economy']
url_soups = []
valuable_texts = []


def find_web_pages(query):
    """method gets the top urls returned by google when making a query"""
    for url in search(query, tld='com', tbs='qdr:m', lang='en', num=10, start=0, stop=10):
        # add the url to the url list.
        url_names.append(url)


def get_url_names():
    """utility method which gives the user the link to each url acquired"""
    return url_names


def create_soups():
    """method creates Beautiful Soup objects which are used to process the html version of the webpages."""
    # iterate through the url list.
    for url in url_names:
        # requesting urls can result in exceptions, use a tru except block to avoid program crashes
        try:
            # get the request object from the webpage.
            req = requests.get(url)
            # get the html format of the page.
            html_version_of_page = req.text
            # create the soup using a parser and add it to the soup list.
            url_soups.append(BeautifulSoup(html_version_of_page, 'lxml'))
        except requests.exceptions.RequestException as e:
            # not necessary to handle the error.
            print(":(")


def tag_valuable(tag):
    """method returns true if the element of the html page is valuable, false otherwise."""
    # we don't want any of the following tags in the processed html.
    if tag.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'footer']:
        return False
    elif isinstance(tag, Comment):
        return False
    return True


def clean_soups():
    """method cleans the Beautiful Soup objects (removes unnecessary tags etc)"""
    for soup in url_soups:
        title = soup.find('title')
        titles.append(title.text)
        # get the entire object
        all_texts = soup.findAll(text=True)
        # filter out the unwanted tags etc
        valuable_text = filter(tag_valuable, all_texts)
        # add the 'valuable text to the list'
        valuable_texts.append(u" ".join(string.strip() for string in valuable_text))


def get_pure_texts():
    """utility method used to find the actual content (as best possible) and print out the contents obtained"""
    counter = 0
    completed_texts = []
    for text in valuable_texts:
        # the "cleaned" text still has many extra spaces, new lines etc.
        # the extra spaces are often found between actual content and menu content etc.
        title_index = find_title_index(text, counter)
        if title_index != -1:
            text = text[title_index:]
        text_chunks = re.split(r'\s{2,}', text)
        completed_texts.append(titles[counter]+'\n')
        # process each chunk.
        for chunk in text_chunks:
            # discard small chunks (may have to adjust based on the formation of the web page)
            if 4000 > len(chunk) > 150 and u'.' in chunk:
                # Some chunks have unnecessary content after the last sentence of the valuable content.
                last_full_stop = chunk.rfind('.')
                completed_texts[counter] += (chunk[0:last_full_stop+1]+'\n')
        counter = counter+1
    return completed_texts


def find_title_index(text, counter):
    my_title = titles[counter].strip()
    title_elements = re.split('[-,|]', my_title)
    try:
        index = text.index(title_elements[0])
        return index
    except ValueError as e:
        return -1


def print_completed_texts():
    for final_text in completed_texts:
        print(final_text+"\n")


