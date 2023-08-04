import requests

from application import ADNSUR

def main():
    r = requests.get("https://adnsur.com.ar")
    html = r.text
    extractor = ADNSUR()
    extractor.extract_content(html)
    for data in extractor.content:
        print(str(data))

if __name__ == "__main__":
    main()
