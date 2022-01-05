from multiprocessing import pool
# from sre_constants import error
from bs4 import BeautifulSoup
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
# import lxml before running

# make a cache pool(temporary storage) which stores the html tags of the website. We keep this so that the indexer can access it and do text analysis.
# instead of uniques we make a cash pools.
q = Queue(maxsize=0)
changes = Queue(maxsize=100000)
cache_pool = Queue(maxsize=10000)
unique = dict()


root_url = ["https://en.wikipedia.org/wiki/Fast_Fourier_transform", "https://www.scrapingbee.com/", "https://www.bbc.com/",
            "https://www.facebook.com", "https://www.google.com/search/howsearchworks/crawling-indexing/", "https://ca.yahoo.com/?p=us&guccounter=1"]
for i in root_url:
    q.put(i)

# q.put(root_url[1])


start_time = time.time()
seconds = 120

rp = Robot.RobotFileParser()

def check(url):
    global unique
    if is_valid_url(url):
        link = urlparse(url)
        domain = link.netloc
        host = link.path

        if unique.get(domain):
            try:
                unique[domain][host]+= 1
                changes.put([url, unique[domain][host]])
                return False
            except KeyError:
                unique[domain][host] = 1
                changes.put([url, 1])
        else:
            temp_dict = {host: 1}
            unique[domain] = temp_dict  # new element
            changes.put([url, 1])
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
        # print("2")
        scheme = link.scheme
        # print("3")
        rp.set_url(scheme + '://' + domain + '/robots.txt')
        # print("4")
        if not rp.can_fetch("*",root_url):
            # print("5")
            r = requests.get(root_url, timeout=(2, 5))
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
                        # print(i)
                        q.put(i)
                    else:
                        pass
                else:
                    pass
        else: 
            print('not allowed')
            pass
    except:
        # print("e")
        return

    

    


def print_results():
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(unique)
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
            pass
            # print("Empty")
        else:
            print("running",end="\r")
            all_url(q.get())
            print("yes",end='\r')


def indexing():
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if cache_pool.empty() == False:
            element = cache_pool.get()
            indexer.htmlparser(element[0], element[1], changes)
        elif elapsed_time > seconds + 30:
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
num_threads = 10
for i in range(num_threads):
    for j in range(30):
        t1 = Thread(target=main_init)
        t1.start()
    t2 = Thread(target=indexing)
    # t1.setDaemon(True)
    # t2.setDaemon(True)

    t2.start()

# print_results()

# t1.close()
# t2.close()
