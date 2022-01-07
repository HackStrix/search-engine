from pymongo import MongoClient
# import psycopg2
from random import randint
import requests
from bs4 import BeautifulSoup
from queue import Queue

# for debugging
from pprint import pprint

# con = psycopg2.connect(database="tags", user="postgres", password="password1234$", host="127.0.0.1", port="5432")

# print("Database opened successfully")
# cur = con.cursor()
# cur.execute('''CREATE TABLE DOMAINS 
#     (URL TEXT PRIMARY KEY NOT NULL,
#     COUNT INT NOT NULL)
# ''')
# con.commit()
# print("table created")

client = MongoClient('mongodb+srv://admin:password1234$@web-map.qzzvr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client["domains"]



def tagparse(data,priority):
    lst_tags = {}
    try:
        for i in data:
            for j in i.text.strip().split(' '):
                if len(j) >= 4:
                    if lst_tags.get(j.lower):
                        x = lst_tags[j.lower()]/priority+1
                        lst_tags[j.lower()] = x*priority
                    else:
                        lst_tags[j.lower()] = 1*priority
                else:
                    pass
        
        return lst_tags

    except:
        return None

def htmlparser(soup, url, changes):
    priorities = [
        tagparse(soup.findAll('h1'), 10), tagparse(soup.findAll('h2'), 9), tagparse(soup.findAll('p'), 8), tagparse(soup.findAll('h3'), 9), tagparse(soup.findAll('li'), 6), tagparse(soup.findAll('b'), 8)
    ]
    while changes.empty() == False:
        lst = changes.get()
        # if db["url"]
    words = {

    }
    # print(priorities)

# r = requests.get("https://www.freecodecamp.org/news/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe/",timeout=(2,5))
# soup = BeautifulSoup(r.content, 'lxml')

# htmlparser(soup, "sdkfvhsakh", None)