import random
import subprocess

import textract
import os.path
import aspose.words as aw

from pdfminer.high_level import extract_text


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
            return subprocess.run(["../djvutxt/djvutxt.exe", path],
                                  stdout=subprocess.PIPE).stdout.decode('utf-8', errors="ignore")

        raise

    def __parse_doc_docx(self, path: str) -> str:
        text = textract.process(path, method='pdfminer')
        return text