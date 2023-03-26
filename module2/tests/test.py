#from ..src.basic_crawler_ import get_unique_domens, get_unique_documents
from module2.src.basic_crawler_ import get_unique_domens, get_unique_documents

def test_get_unique_domens():
    assert get_unique_domens(['gsdsdf']) == []
    assert get_unique_domens(['https:gsdsdf']) == []
    assert get_unique_domens(['https://gsdsdf']) == ['gsdsdf']
    assert get_unique_domens(['http://gsdsdf']) == ['gsdsdf']
    assert get_unique_domens(['https://www.gsdsdf']) == ['gsdsdf']
    assert get_unique_domens(['https:/www.gsdsdf']) == []
    assert get_unique_domens(['https:/.gsdsdf']) == []
    assert get_unique_domens(['https:/gsdsdf']) == []
    assert get_unique_domens(['http://gsdsdf', 'http://gsdsdf']) == ['gsdsdf']
    assert get_unique_domens(['https://gsdsdf', 'http://gsdsdf']) == ['gsdsdf']
    assert get_unique_domens(['https://gsdsdf', 'www.gsdsdf', 'www.gsdsdf/']) == ['gsdsdf']
    assert get_unique_domens(['https://gsdsdf/asd/asdwd/qwr']) == ['gsdsdf']
    assert get_unique_domens(['https://gsdsdf.ru/asd/asdwd/qwr']) == ['gsdsdf.ru']
    assert get_unique_domens(['https://gsds@df']) == []


def test_get_unique_documents():
    assert get_unique_documents(['gsdsdf.pdf']) == []
    assert get_unique_documents(['gsdsdf.pdf', 'gsdsdf.pdf']) == []
    assert get_unique_documents(['https://gsdsdf.pdf']) == ['gsdsdf.pdf']
    assert get_unique_documents(['https://gsdsdf.doc']) == ['gsdsdf.doc']
    assert get_unique_documents(['https://gsdsdf.docx']) == ['gsdsdf.docx']
    assert set(get_unique_documents(['https://gsdsdf.pdf', 'https://gsdsdf.doc', 'https://gsdsdf.docx'])) == \
           {'gsdsdf.docx', 'gsdsdf.doc', 'gsdsdf.pdf'}
    assert get_unique_documents(['gsdsdf.pdf', 'gsdsdf.pdf']) == []
    assert get_unique_documents(['https://gsdsdf.jpg']) == []
    assert get_unique_documents(['https://gsdsdf.pdf', 'https://gsdsdf.jpg', 'https://gsdsdf.docx']) == \
           ['gsdsdf.pdf', 'gsdsdf.docx']
    assert get_unique_documents(['http://gsdsdf.pdf']) == ['gsdsdf.pdf']
    assert get_unique_documents(['http://gsdsdf.doc']) == ['gsdsdf.doc']
    assert get_unique_documents(['http://gsdsdf.docx']) == ['gsdsdf.docx']
    assert get_unique_documents(['www.gsdsdf.pdf']) == ['gsdsdf.pdf']
    assert get_unique_documents(['www.gsdsdf.doc']) == ['gsdsdf.doc']
    assert get_unique_documents(['www.gsdsdf.docx']) == ['gsdsdf.docx']
    assert get_unique_documents(['www.gsdsdf.pdf', 'www.gsdsdf.jpg', 'www.gsdsdf.docx']) == \
           ['gsdsdf.pdf', 'gsdsdf.docx']


