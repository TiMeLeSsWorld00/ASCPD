from module3.src.inverted_index import *


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

def test_gamma_compress():
    assert format(gamma_compress([4, 5]), 'b')[::-1] == '001001'
    assert gamma_compress([4, 5]) == 36

def test_gamma_decompress():
    assert gamma_decompress(36) == [4, 5]

def test_delta_compress():
    assert format(delta_compress([4, 5]), 'b')[::-1] == '011001'
    assert delta_compress([4, 5]) == 38

def test_delta_decompress():
    assert delta_decompress(38) == [4, 5]

def test_search():
    pass

def test_get_text():
    pass



