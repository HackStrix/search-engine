
# import psycopg2
from enum import unique
from pymongo import MongoClient
from random import randint
import requests
from bs4 import BeautifulSoup
from queue import Queue
import math
import re, string
import os
import nltk
from nltk.stem import WordNetLemmatizer


from dotenv import load_dotenv
load_dotenv() 
# for debugging
from pprint import pprint

## for client connecting
if os.environ.get('ENVIRONMENT') == "dev":
    client = MongoClient('mongodb://localhost:27017/')
else:
    client = MongoClient(os.environ.get('ATLAS_URI'))


## Db connect and index creation for unique words
db = client["web-map"]
db.tags.create_index("word", unique=True)

def tagparse(data,priority):
    lst_tags = {}
    try:
        for i in data:
            for j in i.text.strip().split(' '):

                j = re.sub('[%s]' % re.escape(string.punctuation), '', j)
                if len(j) >= 2 and len(j) <=45:

                    if lst_tags.get(j.lower()):
                        x = (lst_tags[j.lower()]/priority) + 1
                        lst_tags[j.lower()] = x*priority
                    else:
                        lst_tags[j.lower()] = priority
                        
                else:
                    pass
        # print(lst_tags)
        return lst_tags

    except:
        return None



def bodyClean(body):
    body = str(body)
    CLEANR = re.compile(r'<[^>]*>')
    cleantext = CLEANR.sub('', body)
    pprint(cleantext)
    ## uncomment this while running for first time ....
    # nltk.download('omw-1.4')
    # nltk.download('wordnet')
    # nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words('english')
    lemmatizer = WordNetLemmatizer()
    doc = re.sub('[^a-zA-Z]', ' ', cleantext)
    doc = doc.lower()
    doc = doc.split()
    doc = [lemmatizer.lemmatize(word) for word in doc if not word in set(stopwords)]
    doc = ' '.join(doc)

    pprint(doc)
    return doc




def htmlparser(soup, url):
    print(soup.findAll('title'))
    print(soup.findAll('meta'))
    bodyClean(soup.find('body'))
    priorities = [
        tagparse(soup.findAll('h1'), 10), tagparse(soup.findAll('h2'), 9), tagparse(soup.findAll('p'), 8), tagparse(soup.findAll('h3'), 9), tagparse(soup.findAll('li'), 7), tagparse(soup.findAll('b'), 8)
    ]
    
    for i in priorities:
        for key, value in i.items():
            # print(key)
            db.tags.update_one(
                filter= { "word": key },
                update= { "$addToSet": { str(math.ceil(value/10)) : url}},
                upsert=True,
                )
