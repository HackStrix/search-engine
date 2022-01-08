
# import psycopg2
from pymongo import MongoClient
from random import randint
import requests
from bs4 import BeautifulSoup
from queue import Queue

# for debugging
from pprint import pprint
client = MongoClient('mongodb://localhost:27017/')
db = client["web-map"]
db.domains.create_index("url",unique=True)
# con = psycopg2.connect(database="tags", user="postgres", password="password1234$", host="127.0.0.1", port="5432")

# print("Database opened successfully")
# cur = con.cursor()
# cur.execute('''CREATE TABLE DOMAINS 
#     (URL TEXT PRIMARY KEY NOT NULL,
#     COUNT INT NOT NULL)
# ''')
# con.commit()
# print("table created")






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

def htmlparser(soup, url, lst):
    # print("running")
    priorities = [
        tagparse(soup.findAll('h1'), 10), tagparse(soup.findAll('h2'), 9), tagparse(soup.findAll('p'), 8), tagparse(soup.findAll('h3'), 9), tagparse(soup.findAll('li'), 6), tagparse(soup.findAll('b'), 8)
    ]
    if lst:
        # print("lol")
        if lst[2] == "new":
            # print("lols")
            try:
                db["domains"].insert_one({
                            "url": lst[0],
                            "count": 1
                        })
                print("r" + "\r")
                
                # if db["domains"].count_documents({"url" : lst[0]}) == 0:
                    
                # else:
                #     print("r" + "\r")
                    
            except:
                db["domains"].update_one({"url" : lst[0]}, {"$set":{"count":lst[1]}})
        else:
            try:
                 db["domains"].update_one({"url" : lst[0]}, {"$set":{"count":lst[1]}})
            except:
                pass
    else:
        pass
        
    words = {

    }
    # print(priorities)

# r = requests.get("https://www.freecodecamp.org/news/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe/",timeout=(2,5))
# soup = BeautifulSoup(r.content, 'lxml')

# htmlparser(soup, "sdkfvhsakh", None)