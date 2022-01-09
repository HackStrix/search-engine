from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime as time
import numpy as np
start = time.now()

client = MongoClient('mongodb+srv://admin:password1234$@web-map.qzzvr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db = client["web-map"]

x = db['tags']


import csv

# x.update_one(
#    filter= { "word": "play" },
#    update= { "$addToSet": { "9" : "https://www.youtube.com/" }},
#    upsert=True,
# )
# time
words = ["technology","python","yahoo"]
z = x.find({ "word": { "$in": words }})

for i in z:
    print(i)
end=time.now()
print(end-start)
# with open('seed_url.csv', newline='') as f:
#     reader = csv.reader(f)
#     url = [row[0] for row in reader]

# z = x.find({ "url": { "$in": url }})
# rank={}
# # id = []
# def lijst(x):
#     return sorted(x.items(), key=lambda x: x[1],reverse=True)
# for i in z:
#     # id.append(i['_id'])
#     rank[i['url']] = i['count']
# print(len(lijst(rank)))
# # print(id)
# end=time.now()
# print(end-start)
# # for i in url:
# #     start = time.now()
# #     z = x.find_one({'url':url})
# #     end = time.now()
# #     timed = end-start
# #     list_time.append(timed)
# #     print(timed)
# # print(np.mean(list_time))
# # start = time.now()
# # z = x.find_one({'url':"www.amazon.com"})
# # end = time.now()
# # print(end-start)
# # start=time.now()
# # y = x.find_one({'_id': ObjectId('61d8ed66b3de40c44097e066')})
# # end=time.now()
# # print(end-start)
# # print(y)
# # print(z)

