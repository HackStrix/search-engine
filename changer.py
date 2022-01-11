from pymongo import MongoClient
client = MongoClient('mongodb+srv://admin:password1234$@web-map.qzzvr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client["web-map"]
db.domains.create_index("url",unique=True)


def changes(lst):
    db.domains.update_one(
        {"url" : lst[0]}, {"$set":{"count": lst[1]}},upsert=True
    )
    # if lst:
    #     if lst[2] == "new":
    #         try:
    #             db["domains"].insert_one({
    #                         "url": lst[0],
    #                         "count": 1
    #                     })
    #             # print("n" + "\r")
                
    #             # if db["domains"].count_documents({"url" : lst[0]}) == 0:
                    
    #             # else:
    #             #     print("r" + "\r")
                    
    #         except Exception as e:
    #             db["domains"].update_one({"url" : lst[0]}, {"$set":{"count":lst[1]}})
    #             # print('x',)
    #     else:
    #         try:
    #              db["domains"].update_one({"url" : lst[0]}, {"$set":{"count":lst[1]}})
    #             #  print("u" + "\r")
    #             #  print('y')
    #         except Exception as e:
    #             # print(e)
    #             pass
                
    # else:
    #     pass
