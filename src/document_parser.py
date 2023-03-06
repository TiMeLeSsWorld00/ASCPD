import random
import subprocess

import textract
import os.path

from win32com import client as wc

from pdfminer.high_level import extract_text


class Document_parser:
    def parse(self, path: str):

        extension = os.path.splitext(path)[1][1:]
        if extension == 'docx':
            return textract.process(path).decode('utf-8')

        if extension == 'doc':
            new_path = path + str(random.randint(1, 100000)) + '.docx'

            w = wc.Dispatch('Word.Application')
            doc = w.Documents.Open(path)
            doc.SaveAs(new_path, 16)
            w.ActiveDocument.Close()
            text = textract.process(new_path).decode('utf-8')
            os.system('del ' + new_path)
            return text

        if extension == 'pdf':
            return extract_text(path)

        if extension == 'djvu':
            return subprocess.run(["../djvutxt/djvutxt.exe", path],
                                  stdout=subprocess.PIPE).stdout.decode('utf-8', errors="ignore")

        raise

    def __parse_doc_docx(self, path: str) -> str:
        text = textract.process(path, method='pdfminer')
        return text