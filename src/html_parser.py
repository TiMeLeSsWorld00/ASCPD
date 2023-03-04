from typing import List

import requests
from bs4 import BeautifulSoup
import re

class Html_paser:

    def parse_url(self, url: str):
        assert isinstance(url, str)
        self.html_text = requests.get(url).text
        return self.__parse()

    def parse_text(self, html_text: str):
        assert isinstance(html_text, str)
        self.html_text = html_text
        return self.__parse()

    def __parse(self):
        return {"text": self.__get_text(), "links": self.__get_links()}

    def __get_text(self) -> str:
        parsed_html = BeautifulSoup(self.html_text)
        return re.sub(string=parsed_html.text, pattern='\n+', repl='\n')

    def __get_links(self) -> List[str]:
        parsed_html = BeautifulSoup(self.html_text)
        return [a['href'] for a in parsed_html.find_all('a', href=True)]
