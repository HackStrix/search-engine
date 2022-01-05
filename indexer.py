from pymongo import MongoClient
from random import randint
import requests
from bs4 import BeautifulSoup

# for debugging
from pprint import pprint

client = MongoClient('mongodb+srv://admin:password1234$@web-map.qzzvr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
# db=client.business
# names = ['Kitchen','Animal','State', 'Tastey', 'Big','City','Fish', 'Pizza','Goat', 'Salty','Sandwich','Lazy', 'Fun']
# company_type = ['LLC','Inc','Company','Corporation']
# company_cuisine = ['Pizza', 'Bar Food', 'Fast Food', 'Italian', 'Mexican', 'American', 'Sushi Bar', 'Vegetarian']
# for x in range(1, 501):
#     business = {
#         'name' : names[randint(0, (len(names)-1))] + ' ' + names[randint(0, (len(names)-1))]  + ' ' + company_type[randint(0, (len(company_type)-1))],
#         'rating' : randint(1, 5),
#         'cuisine' : company_cuisine[randint(0, (len(company_cuisine)-1))] 
#     }
#     #Step 3: Insert business object directly into MongoDB via insert_one
#     result=db.reviews.insert_one(business)
#     #Step 4: Print to the console the ObjectID of the new document
#     print('Created {0} of 500 as {1}'.format(x,result.inserted_id))
# #Step 5: Tell us that you are done
# print('finished creating 500 business reviews')

def tagparse(data):
    lst_tags = {}
    try:
        for i in data:
            for j in i.text.strip().split(' '):
                if len(j) >= 4:
                    lst_tags[j.lower()] = ''
                else:
                    pass
        
        return list(lst_tags.keys())

    except:
        return None

def htmlparser(soup, url):
    priorities = {
        1:tagparse(soup.findAll('h1')),
        3:tagparse(soup.findAll('p'))
                }
    print(priorities)

r = requests.get("https://www.freecodecamp.org/news/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe/",timeout=(2,5))
soup = BeautifulSoup(r.content, 'lxml')

htmlparser(soup, "sdkfvhsakh")