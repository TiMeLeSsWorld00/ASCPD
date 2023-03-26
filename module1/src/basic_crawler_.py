import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import asyncio

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = []
        self.urls_to_visit = [ self.base_url ]

        #stats
        self.outer_urls = []

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
                self.outer_urls.append(url)

    async def run(self):
        while self.urls_to_visit:
            # if len(self.visited_urls) >= 100:
            #     break
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                await self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

if __name__ == '__main__':

    #https://www.msu.ru/
    #https://spbu.ru

    ioloop = asyncio.get_event_loop()
    tasks = [ioloop.create_task(Crawler(base_url= 'https://spbu.ru/').run())]
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()


    # Crawler(base_url= 'https://spbu.ru/').run()