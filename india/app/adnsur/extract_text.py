from bs4 import BeautifulSoup


def extract_text(html: str):
    soup = BeautifulSoup(html, "html.parser")
    soup.find("div")["aria-label"] 
