import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import asyncio
import time

from tqdm import tqdm

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

def get_unique_domens(urls):
    s = set()
    for u in urls:
        if len(u) < 8:
            continue
        if u[:7] == 'http://':
            url = u[7:].split('/')[0]
        elif u[:8] == 'https://':
            url = u[8:].split('/')[0]
        elif u[:4] == 'www.':
            url = u
        else:
            continue

        if url[:4] == 'www.':
            url = url[4:]

        if '@' in url:
            continue
        s.add(url)
    return list(s)

def get_unique_documents(urls):
    s = set()
    for u in urls:
        if len(u) < 8:
            continue
        if u[:7] == 'http://':
            url = u[7:]
        elif u[:8] == 'https://':
            url = u[8:]
        elif u[:4] == 'www.':
            url = u
        else:
            continue

        if url[:4] == 'www.':
            url = url[4:]

        if '@' in url:
            continue

        doc_name = url.split('.')[-1]
        match doc_name:
            case 'pdf':
                s.add(url)
            case 'doc':
                s.add(url)
            case 'docx':
                s.add(url)

    return list(s)

class Crawler:

    def __init__(self, base_url, domen_url):
        self.base_url = base_url
        self.domen_url = domen_url
        self.visited_urls = []
        self.urls_to_visit = [self.base_url]

        #stats
        self.outer_urls = []
        self.domen_urls = []

    def download_url(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        return requests.get(url, headers=headers).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        #print(html, url, soup.find_all('a'))
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    async def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            if url is None:
                continue
            if self.base_url in url:
                self.add_url_to_visit(url)
            else:
                if self.domen_url in url:
                    self.domen_urls.append(url)
                else:
                    self.outer_urls.append(url)

    async def run(self):
        t_start = time.time()
        tqdm_ = tqdm()
        while self.urls_to_visit:
            if time.time() - t_start > 60 * 10:
                break
            # if len(self.visited_urls) >= 100:
            #     break
            tqdm_.update(1)
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                await self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)
        print('CRAWLING DONE')
        print("were visited", len(self.visited_urls))
        print("not visited, but want to", len(self.urls_to_visit))
        print("all inner domens urls: ", len(self.domen_urls))
        print("all outer domens urls: ", len(self.outer_urls))
        du = get_unique_domens(self.domen_urls)
        print("unique inner domens urls: ", len(du), du)
        ou = get_unique_domens(self.outer_urls)
        print("unique outer domens urls: ", len(ou), ou)


        ddu = get_unique_documents(self.domen_urls)
        print("unique documents urls: ", len(ddu), ddu)

        print("общее количество страниц и всех ссылок", len(self.visited_urls) + len(self.urls_to_visit) + len(self.domen_urls) + len(self.outer_urls))
        print("количество внутренних страниц", len(self.visited_urls) + len(self.urls_to_visit))
        print("количество внутренних поддоменов (уникальных)", len(du))
        print("общее количество ссылок на внешние ресурсы", len(self.outer_urls))
        print("количество уникальных внешних ресурсов", len(ou))
        print("количество уникальных ссылок на файлы doc/docx/pdf", len(ddu))
        print("количество неработающих страниц", "????????????????")

if __name__ == '__main__':

    #https://www.msu.ru/
    #https://spbu.ru

    ioloop = asyncio.get_event_loop()
    tasks = [ioloop.create_task(Crawler(base_url= 'https://spbu.ru/', domen_url= 'spbu.ru').run())]
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()


    # Crawler(base_url= 'https://spbu.ru/').run()