import random

import textract
import os.path
import aspose.words as aw
import zipfile
import xml.etree.ElementTree as ET
from PIL import Image
import DjvuRleImagePlugin

from pdfminer.high_level import extract_text

from tqdm import tqdm

import bz2

class Document_parser:
    def parse(self, path: str):

        extension = os.path.splitext(path)[1][1:]
        if extension == 'docx':
            return textract.process(path).decode('utf-8')

        if extension == 'doc':
            doc = aw.Document(path)
            r = random.randint(1, 10000)
            doc.save(path + str(r) + '.docx')
            return textract.process(path + str(r) + '.docx').decode('utf-8')

        if extension == 'pdf':
            return extract_text(path)

        if extension == 'djvu':
            # doc = aw.Document(path)
            # r = random.randint(1, 10000)
            # doc.save(path + str(r) + '.jpeg')
            # im = Image.open(path)
            r = DjvuRleImagePlugin.DjvuRleDecoder(path)
            print(r.decode(asdf))
            # return textract.process(path + str(r) + '.docx').decode('utf-8')
            # with open(path, 'rb') as f:
            #     data = [f.read(999999)]
            #     for i in tqdm(data):
            #         for j in tqdm(range(0, len(i))):
            #             for k in range(j, len(i), 20):
            #                 if len(i[j:k]) > 0:
            #                     try:
            #                         # print(i.decode('utf-8'))
            #                         a = bz2.decompress(i[j:k])
            #                         print(a)
            #                     except:
            #                         pass
            return
        raise

    def __parse_doc_docx(self, path: str) -> str:
        text = textract.process(path, method='pdfminer')
        return text