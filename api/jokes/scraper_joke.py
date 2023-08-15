import requests
from random import randint
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
def scrapping():
    ua = UserAgent()
    headers = {
        'User-agent':ua.random
    }
    i = randint(1, 4)
    URL = f"https://www.mk.ru/anekdoti/{i}/"
    response = requests.get(URL, headers=headers)
    bs4 = BeautifulSoup(response.text, 'lxml')
    joke = bs4.findAll('p', class_="listing-preview__desc")
    j = randint(1, 29)
    jokes = joke[j].text.strip()
    return jokes

def main():
    print(scrapping())

if __name__=="__main__":
    main()
