import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import time

from tqdm import tqdm
import json
import validators

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

def is_document(url):
    doc_name = url.split('.')[-1]
    if doc_name.lower() in ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'djvu', 'bmp', 'raw',
                            'ppt', 'pptx', 'xsl', 'xlsx', 'gif', 'webp', 'zip', 'rar', 'gz',
                            '3gp', 'avi', 'mov', 'mp4', 'm4v', 'm4a', 'mp3', 'mkv', 'ogv', 'ogm',
                            'webm', 'wav', 'txt', 'rtf']:
        return True
    return False

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
            url = u.split('/')[0]
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

        if url.split('.')[-1] in ['pdf', 'doc', 'docx']:
            s.add(url)

    return list(s)

class Crawler:

    def __init__(self, base_url = '', domen_url = ''):
        self.base_url = base_url
        self.domen_url = domen_url
        self.visited_urls = set()
        self.urls_to_visit = set()
        self.urls_to_visit.add(self.base_url)

        #stats
        self.outer_urls = []
        self.domen_urls = []
        self.non_working_url = []

    def download_url(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        return requests.get(url, headers=headers).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls:
            self.urls_to_visit.add(url)

    def crawl(self, url):
        if is_document(url):
            return
        html = self.download_url(url)
        for u in self.get_linked_urls(url, html):
            if (u is None) or (not validators.url(u)):
                self.non_working_url.append(u)
                continue
            if self.base_url in u:
                self.add_url_to_visit(u)
            else:
                if self.domen_url in u:
                    self.domen_urls.append(u)
                else:
                    self.outer_urls.append(u)

    def run(self):
        t_start = time.time()
        tqdm_ = tqdm()
        while self.urls_to_visit:
            if time.time() - t_start > 66666*60 * 10:
                break
            tqdm_.update(1)
            url = self.urls_to_visit.pop()
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
                self.non_working_url.append(url)
            finally:
                self.visited_urls.add(url)
                logging.info(f'Rest: {len(self.urls_to_visit)}')

        print('CRAWLING DONE')
        self.print_stats()

        return self

    def to_csv(self, name: str):
        df = dict()
        df['base_url'] = self.base_url
        df['domen_url'] = self.domen_url
        df['visited_urls'] = list(self.visited_urls)
        df['urls_to_visit'] = list(self.urls_to_visit)
        df['outer_urls'] = list(self.outer_urls)
        df['domen_urls'] = list(self.domen_urls)
        df['non_working_url'] = list(self.non_working_url)

        with open(name, 'w') as convert_file:
            convert_file.write(json.dumps(df, indent=4))

    def from_csv(self, name: str):
        with open(name, 'r') as convert_file:
            df = json.load(convert_file)

        self.base_url = df['base_url']
        self.domen_url = df['domen_url']
        self.visited_urls = set(df['visited_urls'])
        self.urls_to_visit = set(df['urls_to_visit'])
        self.outer_urls = df['outer_urls']
        self.domen_urls = df['domen_urls']
        self.non_working_url = df['non_working_url']

        return self


    def print_stats(self):
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

        print("общее количество страниц и всех ссылок",
              len(self.visited_urls) + len(self.urls_to_visit) + len(self.domen_urls) + len(self.outer_urls))
        print("количество внутренних страниц", len(self.visited_urls) + len(self.urls_to_visit))
        print("количество внутренних поддоменов (уникальных)", len(du))
        print("общее количество ссылок на внешние ресурсы", len(self.outer_urls))
        print("количество уникальных внешних ресурсов", len(ou))
        print("количество уникальных ссылок на файлы doc/docx/pdf", len(ddu))
        print("количество неработающих страниц", len(self.non_working_url), "уникальных",
              len(set(self.non_working_url)))


if __name__ == '__main__':

    #https://www.msu.ru/
    #https://spbu.ru/

    Crawler(base_url= 'https://www.msu.ru/', domen_url= 'msu.ru').run().to_csv('msu.csv')
    Crawler().from_csv('msu.csv').print_stats()

    # Crawler(base_url= 'https://spbu.ru/').run()