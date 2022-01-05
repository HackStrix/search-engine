from multiprocessing import pool
from bs4 import BeautifulSoup
import re 
import requests
import urllib.request, urllib.parse, urllib.error
from queue import Queue
import time
import sys
from multiprocessing.pool import ThreadPool as Pool
import indexer
from threading import Thread
# import lxml before running

# make a cache pool(temporary storage) which stores the html tags of the website. We keep this so that the indexer can access it and do text analysis. 
# instead of uniques we make a cash pools. 
q = Queue(maxsize= 0)
cache_pool = Queue(maxsize=10000)
unique = dict()


root_url = ["https://en.wikipedia.org/wiki/Fast_Fourier_transform", "https://www.scrapingbee.com/", "https://www.bbc.com/","https://www.facebook.com", "https://www.google.com/search/howsearchworks/crawling-indexing/", "https://ca.yahoo.com/?p=us&guccounter=1"]
for i in root_url:
    q.put(i)


start_time = time.time()
seconds = 120

def check(url):
    global unique
    if is_valid_url(url):
        try:
            unique[url]
            return False
        except KeyError:
            unique[url] = '' # new element
            return True
        

def is_valid_url(url):
    # regex = re.compile(
    #     r'^https?://'  # http:// or https://
    #     r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
    #     r'localhost|'  # localhost...
    #     r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    #     r'(?::\d+)?'  # optional port
    #     r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    

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
    # return url is not None and regex.search(url)



def all_url(root_url):
    global q
    global unique
    

    try:
        r = requests.get(root_url,timeout=(2,5))
        
    except:
        return 

    soup = BeautifulSoup(r.content, 'lxml')
    cache_pool.put([soup, root_url])
    fill = soup.findAll('a')
    lst = []

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
                print(i)
                q.put(i)
            else:
                pass
        else:
            pass
    


def print_results(): 
    print(len(unique))
    print(q.qsize())
    print(sys.getsizeof(unique))

def main_init():
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > seconds:
            break
        
        if q.empty():
            print("Empty")
        else:
            all_url(q.get())
def indexing():
    while True:
        if cache_pool.empty() == False:
            indexer.htmlparser(cache_pool.get()[0], cache_pool.get()[1])
        else:
            print("Cache pool empty")




# def pooling():
#     pool_size = 100  # your "parallelness"

#     pool = Pool(pool_size)

#     for i in range(pool_size):
#         pool.apply_async(indexing,( ))
#         pool.apply_async(main_init, ( ))
    

    # pool.close()
    # pool.join()
num_threads = 1
for i in range(num_threads):
    for j in range(30):
        t1 = Thread(target= main_init)
        t1.start()
    t2 = Thread(target= indexing)
    # t1.setDaemon(True)
    # t2.setDaemon(True)
    
    t2.start()

t1.close()
t2.close()

