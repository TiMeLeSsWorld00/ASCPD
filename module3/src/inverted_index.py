from collections import defaultdict
import logging
from typing import List
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import time


from tqdm import tqdm
import json
import validators
import re
import spacy
import ru_core_news_sm
model_ru = ru_core_news_sm.load()
import copy

INDEX = defaultdict(list)
DOCS = dict()


def is_document(url):
    doc_name = url.split('.')[-1]
    if doc_name.lower() in ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'djvu', 'bmp', 'raw',
                            'ppt', 'pptx', 'xsl', 'xlsx', 'gif', 'webp', 'zip', 'rar', 'gz',
                            '3gp', 'avi', 'mov', 'mp4', 'm4v', 'm4a', 'mp3', 'mkv', 'ogv', 'ogm',
                            'webm', 'wav', 'txt', 'rtf']:
        return True
    return False


def download_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    return requests.get(url, headers=headers).text


def get_text(html_text) -> List[str]:
    parsed_html = BeautifulSoup(html_text)
    text = re.findall(pattern='[А-Яа-я]+', string=parsed_html.text)
    text = ' '.join(text).lower()
    text = [t.lemma_ for t in model_ru(text) if (len(t) > 1)]
    return text


def run(urls_to_visit: List[str]):
    t_start = time.time()
    index = 0
    for url in tqdm(urls_to_visit[:40000]):
        index += 1
        # if index > 100:
        #     break
        time_consumed = time.time() - t_start
        # if time_consumed > 60 * 5:
        #     break
        # print('index', index, '\ttime', time_consumed, '\turl', url, end=' ')
        try:
            if is_document(url):
                continue
            html = download_url(url)
            if html:
                # with open(f'../Index/{self.counterIndex}.txt', 'w', encoding='utf-8') as f:
                #     f.write(self.__get_text(html))
                text = get_text(html)
                add_to_index(text, url)
        except Exception:
            # print('\tbroken')
            pass
        finally:
            # print('\tdone')
            pass

    print('INDEXING DONE')

def add_to_index(doc: List[str], url: str):
    global INDEX, DOCS

    next_id = len(DOCS)
    DOCS[next_id] = url

    words = set(doc)
    for word in words:
        INDEX[word].append(next_id)

    return


def search(request: str, decom=None):
    request = request.lower()
    words = [t.lemma_ for t in model_ru(request) if (len(t) > 1)]

    match decom:
        case None:
            start = set(INDEX[words[0]])
            for i in range(1, len(words)):
                start = start.intersection(set(INDEX[words[i]]))
        case "gamma":
            start = set(gamma_decompress(INDEX[words[0]]))
            for i in range(1, len(words)):
                start = start.intersection(set(gamma_decompress(INDEX[words[i]])))
            return start
        case "delta":
            start = set(delta_decompress(INDEX[words[0]]))
            for i in range(1, len(words)):
                start = start.intersection(set(delta_decompress(INDEX[words[i]])))
            return start
    return None


def gamma_compress(numbers: List[int]) -> int:
    bitstream = []
    previous_number = 0
    for number in numbers:
        delta = number - previous_number  # store deltas, much smaller numbers
        N = delta.bit_length() - 1
        encoded_number = bin(delta)[2:][::-1] + '0' * N
        bitstream.append(encoded_number)
        previous_number = number
    bitstream.reverse()
    return int(''.join(bitstream), 2)


def gamma_decompress(com_numbers: int) -> List[int]:
    numbers = []

    bitstream = list(format(com_numbers, 'b'))
    bitstream.reverse()

    read_zeros = True
    N = 1
    number = []
    previous_number = 0
    for bit in bitstream:
        if read_zeros:
            if bit == '0':
                N += 1
                continue
            else:
                read_zeros = False
        number.append(bit)
        N -= 1
        if N == 0:
            read_zeros = True
            N = 1
            numbers.append(previous_number + int(''.join(number), 2))
            previous_number = numbers[-1]
            number = []
    return numbers


def delta_compress(numbers: List[int]) -> int:
    bitstream = []
    previous_number = 0
    for number in numbers:
        delta = number - previous_number  # store deltas, much smaller numbers
        N = delta.bit_length()
        M = N.bit_length() - 1
        encoded_N = '0' * M + format(N, 'b')[:]
        encoded_number = format(delta, 'b')[1:]
        res = encoded_N + encoded_number
        bitstream.append(res[::-1])
        previous_number = number
    bitstream.reverse()
    return int(''.join(bitstream), 2)


def delta_decompress(com_numbers: int) -> List[int]:
    numbers = []

    bitstream = list(format(com_numbers, 'b'))
    bitstream.reverse()

    read_zeros = True
    N = 1
    M = None
    number_N = []
    number = ['1']
    previous_number = 0
    for bit in bitstream:
        if read_zeros:
            if bit == '0':
                N += 1
                continue
            else:
                read_zeros = False
        if M is None:
            number_N.append(bit)
            N -= 1
        else:
            number.append(bit)
            M -= 1
        if N == 0:
            if M is None:
                M = int(''.join(number_N), 2) - 1
            if M == 0:
                read_zeros = True
                N = 1
                M = None
                numbers.append(previous_number + int(''.join(number), 2))
                previous_number = numbers[-1]
                number_N = []
                number = ['1']

    return numbers

def urls_from_csv(name: str):
    with open(name, 'r') as convert_file:
        df = json.load(convert_file)

    return list(df['visited_urls'])

if __name__ == '__main__':
    urls = urls_from_csv("msu.csv")
    run(urls)

    with open("INDEX.json", "w", encoding='utf-8') as outfile:
        json.dump(INDEX, outfile, indent=1)

    with open("DOCS.json", "w", encoding='utf-8') as outfile:
        json.dump(DOCS, outfile, indent=1)

    INDEX_copy_gamma = copy.deepcopy(INDEX)
    INDEX_copy_delta = copy.deepcopy(INDEX)
    for i, v in INDEX.items():
        INDEX_copy_gamma[i] = gamma_compress(v)
    with open("index_gamma.json", "w", encoding='utf-8') as outfile:
        json.dump(INDEX_copy_gamma, outfile, indent=1)

    for i, v in INDEX.items():
        INDEX_copy_delta[i] = delta_compress(v)
    with open("index_delta.json", "w", encoding='utf-8') as outfile:
        json.dump(INDEX_copy_delta, outfile, indent=1)