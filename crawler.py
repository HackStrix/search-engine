from multiprocessing import pool
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re
import requests
import urllib.request
import urllib.error
from urllib.parse import urlparse
import urllib.robotparser as Robot
from queue import Queue
import time
import sys
from multiprocessing.pool import ThreadPool as Pool
import indexer
from threading import Thread
import pprint
import changer
# from numba import jit, cuda
# import lxml before running

# make a cache pool(temporary storage) which stores the html tags of the website. We keep this so that the indexer can access it and do text analysis.
# instead of uniques we make a cash pools.
q = Queue(maxsize=0)
changes = Queue(maxsize=0)
cache_pool = Queue(maxsize=10000)
unique = dict()
# client = MongoClient('mongodb+srv://admin:password1234$@web-map.qzzvr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
# client = MongoClient('mongodb://localhost:27017/')



root_url = ["https://en.wikipedia.org/wiki/Fast_Fourier_transform", "https://www.bbc.com/",
            "https://www.facebook.com", "https://www.google.com/search/howsearchworks/crawling-indexing/", "https://ca.yahoo.com/?p=us&guccounter=1"]
root_url=["http://localhost:8000"]
for i in root_url:
    q.put(i)
# import csv

# with open('seed_url.csv', newline='') as f:
#     reader = csv.reader(f)
#     root_url = ["https://"+row[0] for row in reader]
# # print(data)
# # print(1+"aa")
# for i in root_url:
#     q.put(i)

# q.put(root_url[1])


start_time = time.time()
seconds = 120
words = dict()


# @jit(target="cuda")
def check(url):
    global unique
    if is_valid_url(url):
        link = urlparse(url)
        domain = link.netloc
        host = link.path
        # print(url)
        if unique.get(domain):
            try:
                unique[domain][host] +=1
                unique[domain]['__0__']+=1
                x = unique[domain]['__0__']
                if x > 10:
                    if x%200 == 0:
                        changes.put([domain, unique[domain]['__0__'], "upd"])
                    elif x<200 and x%20 == 0:
                        changes.put([domain, unique[domain]['__0__'], "upd"])
                else:
                    changes.put([domain, unique[domain]['__0__'], "upd"])
                    # pass
                return False
            except KeyError:
                unique[domain]['__0__']+=1
                unique[domain][host] = 1
                x = unique[domain]['__0__']
                if x > 10:
                    if x%200 == 0:
                        changes.put([domain, unique[domain]['__0__'], "upd"])
                    elif x<200 and x%20 == 0:
                        changes.put([domain, unique[domain]['__0__'], "upd"])
                else:
                    changes.put([domain, unique[domain]['__0__'], "upd"])
                    # pass
                return False
        else:
            unique[domain] = {'__0__':1}
            # temp_dict = {host: 1}
            unique[domain][host] = 1  # new element
            changes.put([domain, unique[domain]['__0__'],"new"])
            return True


def is_valid_url(url):
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
    p = re.compile(regex)
    if(re.search(p, url)):
        return True
    else:
        return False


def all_url(root_url):
    global q
    global unique

    try:
        link = urlparse(root_url)
        # print("1")
        domain = link.netloc
        # print("domain")
        scheme = link.scheme
        # print("scheme")
        combined_str = scheme + '://' + domain + '/robots.txt'
        # print(combined_str)
        rp = Robot.RobotFileParser()
        rp.set_url(combined_str)
        # print("hello")
        try:
            # print("his")
            rp.read()
            # print("how")
            boolean = rp.can_fetch("*",root_url)
        except:
            # print("helloo")
            boolean=True
        # print("4")
        # print(boolean)
        if boolean:
            r = requests.get(root_url, timeout=(3, 5))
            # print(r)
            soup = BeautifulSoup(r.content, 'lxml',from_encoding="iso-8859-1")
            cache_pool.put([soup, root_url])
            fill = soup.findAll('a')
            lst = []
            # print(fill)
            for i in fill:
                lst.append(i.get('href'))

            for i in lst:
                if i:
                    regex1 = ("(^\/[a-zA-Z*%$!)(\/&*]*)")
                    p1 = re.compile(regex1)
                    if(re.search(p1, i)):
                        if root_url[-1] == "/":
                            i = root_url + i[1:]
                        else:
                            i = root_url + i
                    if check(i):
                        # print(i)
                        q.put(i)
                    else:
                        pass
                else:
                    pass
        else: 
            # print('not allowed')
            pass
    except:
        pass
        # print("e")

    

    


def print_results():
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(unique)
    # print(len(unique))
    print("queue size :"+str(q.qsize()))
    print("memory :"+str(sys.getsizeof(unique)))
    print("cachepool :"+str(cache_pool.qsize()))
    print("changes :"+str(changes.qsize()))


def main_init():
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        # print(int(elapsed_time),end='\r')
        if elapsed_time > seconds:
            break

        if q.empty():
            pass
            # print("Empty")
        else:
            
            all_url(q.get())
            print('domains crawled : %10s %1s'%(str(len(unique)),"|"),end="\r")
            print('domains crawled : %10s %1s'%(str(len(unique)),"/"),end="\r")
            print('domains crawled : %10s %1s'%(str(len(unique)),"-"),end="\r")

            # print(str(len(unique))+"   /",end="\r")
            # print(str(len(unique))+"   -",end="\r")


def indexing():
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time < seconds + 300:
            if cache_pool.empty() == False:
                print('indexing Left : %10s %1s'%(str(cache_pool.qsize()),"*"),end="\r\t\t\t\t\t")
                element = cache_pool.get()
                indexer.htmlparser(element[0], element[1])
        else:
            print_results()
            break
            # print("Cache pool empty")
def changing():
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time <= seconds + 300:
            if changes.empty() == False:
                print('Changes Left : %10s %1s'%(str(changes.qsize()),"*"),end="\r\t\t\t\t\t")
                element = changes.get()
                changer.changes(element)
        elif elapsed_time > seconds + 300:
            print_results()
            break
        else:
            pass
            # print("Cache pool empty")

# def pooling():
#     pool_size = 100  # your "parallelness"

#     pool = Pool(pool_size)

#     for i in range(pool_size):
#         pool.apply_async(indexing,( ))
#         pool.apply_async(main_init, ( ))
    # pool.close()
    # pool.join()
num_threads = 1
threads = []
for i in range(num_threads):
    for j in range(1):
        t1 = Thread(target=changing)
        t3 = Thread(target=indexing)
        threads.append(t1)
        t1.start()
        t3.start()
    t2 = Thread(target=main_init)
    threads.append(t2)
    t2.setDaemon(True)
    t2.start()

# for x in threads:
#     x.join()
#     pp = pprint.PrettyPrinter(indent=4)
#     pp.pprint(unique)
# t1.close()
# t2.close()
