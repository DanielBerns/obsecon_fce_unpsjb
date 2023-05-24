from bs4 import BeautifulSoup

def extract_text(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    noclean_text = soup.get_text("-xxx-")
    
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in noclean_text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text, noclean_text # text.encode('utf-8')

import requests

def get_adn():
    adn = "https://www.adnsur.com.ar/"
    r = requests.get(adn)
    return r.content
    
