from email.mime import base
import multiprocessing
import time
import queue
import requests

from urllib import response
from bs4 import BeautifulSoup
from pathlib import Path

requests.adapters.DEFAULT_RETRIES = 10


def change_url(base_url):
    if not base_url.startswith("https://"):
        base_url = 'https://' + base_url    
    
    return base_url

def crawl(base_url, duration=10, start_anchor='/'):
    base_url = change_url(base_url)
    start = time.time()
    urls = []
    file_urls = []
    search_anchors = queue.Queue()
    while True:
        if time.time() - start > duration:
            return urls, file_urls

        if not start_anchor:
            start_anchor = '/'
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/86.0.4240.111 Safari/537.36'}
        print("---- Requesting: ", base_url + start_anchor)
        try:
            response = requests.request('GET', base_url + start_anchor, headers=headers, timeout=(2,5))
            print("---- Request Completed!")
        except:
            try: 
                response = requests.request('GET', base_url + start_anchor, headers=headers, timeout=(2,5))
            except:
                print("!!!!! Request Failed!")
                continue            
        soup = BeautifulSoup(response.text, 'lxml')
        anchors = find_local_anchor(soup, base_url, start_anchor)
        if anchors:
            for a in anchors:
                url = base_url + a
                if url in urls or url in file_urls:
                    continue
                if Path(a).suffix:
                    file_urls.append(url)
                else:
                    search_anchors.put(a)                
                    urls.append(url)
                print(url)
        if search_anchors.empty():
            break
        start_anchor = search_anchors.get()        
    print("Crawl Finished!")
    return urls, file_urls


def find_local_anchor(soup, base_url, start_anchor):
    anchors = []    
    www_base_url = base_url.replace('https://', 'https://www.')
    for link in soup.find_all('a'):
        anchor = link.attrs['href'] if "href" in link.attrs else ''
        if anchor.startswith(base_url):            
            anchors.append(anchor.replace(base_url, ''))
        elif anchor.startswith(start_anchor):
            anchors.append(anchor)
        elif anchor.startswith(www_base_url):            
            anchors.append(anchor.replace(www_base_url, ''))
        
    return anchors


# p = multiprocessing.Process(target=crawl, name="crawl", args=(BASE_URL,''))
# p.start()
# p.join(10)

# # If thread is active
# if p.is_alive():
#     print("Crawl is running... let's kill it...")

#     # Terminate foo
#     p.terminate()
#     p.join()
# start = time.time()
# urls = crawl(BASE_URL)
# end = time.time()
# print("Done!")
# print("Real Running Time: ", end - start)
# urls = crawl('https://vietnamworks.com', duration=10, start_anchor='/')
# print(urls)