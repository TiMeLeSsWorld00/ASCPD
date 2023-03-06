from document_parser import Document_parser
import pathlib

if __name__ == '__main__':
    print(Document_parser().parse(str(pathlib.Path("../data/doc.doc").resolve())))