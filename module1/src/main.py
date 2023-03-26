from document_parser import Document_parser
import pathlib

from src.html_parser import Html_paser

if __name__ == '__main__':
    print(Document_parser().parse(str(pathlib.Path("../data/djvu.djvu").resolve())))
    print(Html_paser().parse_url('https://gzmland.ru/'))
