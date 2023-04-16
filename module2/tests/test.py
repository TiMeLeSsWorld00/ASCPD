#from ..src.basic_crawler_ import get_unique_domens, get_unique_documents
from module2.src.basic_crawler_ import get_unique_domens, get_unique_documents, is_document, Crawler

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
    assert set(get_unique_documents(['https://gsdsdf.pdf', 'https://gsdsdf.doc', 'https://gsdsdf.docx']))== \
           {'gsdsdf.docx', 'gsdsdf.doc', 'gsdsdf.pdf'}
    assert get_unique_documents(['gsdsdf.pdf', 'gsdsdf.pdf']) == []
    assert get_unique_documents(['https://gsdsdf.jpg']) == []
    assert set(get_unique_documents(['https://gsdsdf.pdf', 'https://gsdsdf.jpg', 'https://gsdsdf.docx'])) == \
           {'gsdsdf.pdf', 'gsdsdf.docx'}
    assert get_unique_documents(['http://gsdsdf.pdf']) == ['gsdsdf.pdf']
    assert get_unique_documents(['http://gsdsdf.doc']) == ['gsdsdf.doc']
    assert get_unique_documents(['http://gsdsdf.docx']) == ['gsdsdf.docx']
    assert get_unique_documents(['www.gsdsdf.pdf']) == ['gsdsdf.pdf']
    assert get_unique_documents(['www.gsdsdf.doc']) == ['gsdsdf.doc']
    assert get_unique_documents(['www.gsdsdf.docx']) == ['gsdsdf.docx']
    assert set(get_unique_documents(['www.gsdsdf.pdf', 'www.gsdsdf.jpg', 'www.gsdsdf.docx'])) == \
           {'gsdsdf.pdf', 'gsdsdf.docx'}

def test_is_document():
    assert is_document('gsdsdf.pdf') == True
    assert is_document('gsdsdf.PdF') == True
    assert is_document('gsdsdf.pDf') == True
    assert is_document('gsdsdf.pDf.heh') == False
    assert is_document('gsdsdfpdf') == False
    #assert is_document('pdf') == False
    #assert is_document('.pdf') == False
    #assert is_document('gsdsdf.pdf.') == True
    assert is_document('gsdsdf.doc') == True
    assert is_document('gsdsdf.docx') == True
    assert is_document('gsdsdf.jpg') == True
    assert is_document('gsdsdf.jpeg') == True
    assert is_document('gsdsdf.png') == True
    assert is_document('gsdsdf.djvu') == True
    assert is_document('gsdsdf.bmp') == True
    assert is_document('gsdsdf.raw') == True
    assert is_document('gsdsdf.ppt') == True
    assert is_document('gsdsdf.pptx') == True
    assert is_document('gsdsdf.xsl') == True
    assert is_document('gsdsdf.xlsx') == True
    assert is_document('gsdsdf.gif') == True
    assert is_document('gsdsdf.webp') == True
    assert is_document('gsdsdf.zip') == True
    assert is_document('gsdsdf.rar') == True
    assert is_document('gsdsdf.gz') == True
    assert is_document('gsdsdf.3gp') == True
    assert is_document('gsdsdf.avi') == True
    assert is_document('gsdsdf.mov') == True
    assert is_document('gsdsdf.mp4') == True
    assert is_document('gsdsdf.m4v') == True
    assert is_document('gsdsdf.m4a') == True
    assert is_document('gsdsdf.mp3') == True
    assert is_document('gsdsdf.mkv') == True
    assert is_document('gsdsdf.ogv') == True
    assert is_document('gsdsdf.ogm') == True
    assert is_document('gsdsdf.webm') == True
    assert is_document('gsdsdf.wav') == True
    assert is_document('gsdsdf.txt') == True
    assert is_document('gsdsdf.rtf') == True


def test_add_url_to_visit():
    c = Crawler()
    c.add_url_to_visit('https//www.spbu.ru')
    assert c.urls_to_visit == {'', 'https//www.spbu.ru'}
    c.add_url_to_visit('https//www.msu.ru')
    assert c.urls_to_visit == {'', 'https//www.spbu.ru', 'https//www.msu.ru'}
    c.add_url_to_visit('https//www.msu.ru')
    assert c.urls_to_visit == {'', 'https//www.spbu.ru', 'https//www.msu.ru'}
    c.add_url_to_visit('https//www.spbu.ru')
    assert c.urls_to_visit == {'', 'https//www.spbu.ru', 'https//www.msu.ru'}


def test_crawl():
    c = Crawler(base_url='spbu.ru', domen_url='spbu.ru')
    c.crawl('heh.pdf')
    assert c.visited_urls == set()
    c.crawl("https://www.msu.ru/")
    assert c.visited_urls == set()
    assert len(c.outer_urls) > 0
    assert c.domen_urls == []

def test_run():
    c = Crawler()
    c.run()
    assert c.non_working_url == ['']
    b = Crawler(base_url='heh.pdf')
    b.run()
    assert c.visited_urls == {''}

def test_download_url():
    c = Crawler()
    c.download_url("https://www.msu.ru/")
    assert len(c.urls_to_visit) > 0

def test_get_linked_urls():
    c = Crawler()
    try:
        c.get_linked_urls('', '')
    except:
        assert False




