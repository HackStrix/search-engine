
# import psycopg2
from enum import unique
from pymongo import MongoClient
from random import randint
import requests
from bs4 import BeautifulSoup
from queue import Queue
import math

# for debugging
from pprint import pprint
# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient('mongodb+srv://admin:password1234$@web-map.qzzvr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db = client["web-map"]
db.domains.create_index("url",unique=True)
db.tags.create_index("word", unique=True)



def changes(lst):
    if lst:
        if lst[2] == "new":
            try:
                db["domains"].insert_one({
                            "url": lst[0],
                            "count": 1
                        })
                # print("n" + "\r")
                
                # if db["domains"].count_documents({"url" : lst[0]}) == 0:
                    
                # else:
                #     print("r" + "\r")
                    
            except Exception as e:
                db["domains"].update_one({"url" : lst[0]}, {"$set":{"count":lst[1]}})
                # print('x',)
        else:
            try:
                 db["domains"].update_one({"url" : lst[0]}, {"$set":{"count":lst[1]}})
                #  print("u" + "\r")
                #  print('y')
            except Exception as e:
                # print(e)
                pass
                
    else:
        pass


def tagparse(data,priority):
    lst_tags = {}
    try:
        for i in data:
            for j in i.text.strip().split(' '):
                if len(j) >= 4:
                    if lst_tags.get(j.lower):
                        x = (lst_tags[j.lower()]/priority)+1
                        lst_tags[j.lower()] = x*priority
                    else:
                        lst_tags[j.lower()] = 1*priority
                        
                else:
                    pass
        
        return lst_tags

    except:
        return None

def htmlparser(soup, url):
    # print("running")
    priorities = [
        tagparse(soup.findAll('h1'), 10), tagparse(soup.findAll('h2'), 9), tagparse(soup.findAll('p'), 8), tagparse(soup.findAll('h3'), 9), tagparse(soup.findAll('li'), 7), tagparse(soup.findAll('b'), 8)
    ]
    
    for i in priorities:
        for key, value in i.items():
            db.tags.find_one_and_update(
                filter= { "word": key },
                update= { "$addToSet": { str(math.ceil(value)) : url}},
                upsert=True,
                )
    # print(priorities)

# r = requests.get("https://www.freecodecamp.org/news/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe/",timeout=(2,5))
# soup = BeautifulSoup(r.content, 'lxml')

# htmlparser(soup, "https://www.freecodecamp.org/news/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe/", None, None)