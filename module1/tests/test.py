import pathlib

import pytest

from src.document_parser import Document_parser
from src.html_parser import Html_paser
import requests

def test_html_parser():
    assert Html_paser().parse_url('https://gzmland.ru/') == {'text': '\nÐ\x9fÑ\x83Ñ\x81Ñ\x82Ð¾Ð¹ Ñ\x81Ð°Ð¹Ñ\x82\nÐ¡Ð¾Ð²ÐµÑ\x80Ñ\x88ÐµÐ½Ð½Ð¾ Ð¿Ñ\x83Ñ\x81Ñ\x82Ð¾Ð¹ Ñ\x81Ð°Ð¹Ñ\x82.\nThis site is absolutely empty.\nÐ\x97Ð´ÐµÑ\x81Ñ\x8c Ð½Ð¸Ñ\x87ÐµÐ³Ð¾ Ð½ÐµÑ\x82.\nThere is nothing here.\n', 'links': []}
    assert Html_paser().parse_text(requests.get('https://s-f.ca/').text) == Html_paser().parse_url('https://s-f.ca/')

def test_docomunts_parser():
    path_doc = "../data/doc.doc"
    path_docx = "../data/docx.docx"
    path_pdf = "../data/pdf.pdf"
    path_djvu = "../data/djvu.djvu"

    assert Document_parser().parse(str(pathlib.Path(path_doc).resolve())) == "Hello, My dear friends\\n\\n"
    assert Document_parser().parse(str(pathlib.Path(path_docx).resolve())) == "Hello, My dear friends"
    assert Document_parser().parse(str(pathlib.Path(path_pdf).resolve())) == "Hello, My dear friends \n\n \n\n\x0c"
    assert Document_parser().parse(str(pathlib.Path(path_djvu).resolve())).find("documents and applied several parts of E.O. 12866 to guidance documents,") != -1
