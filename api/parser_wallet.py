import requests
import xmltodict
def scrapping():
    URL = 'http://www.cbr.ru/scripts/XML_daily.asp'
    r = requests.get(URL)
    data = r.text
    data = xmltodict.parse(data)
    ID = ["R01235", "R01239", "R01820", "R01090B"]
    wallets = dict()
    for item in data["ValCurs"]['Valute']:
        for id in ID:
            if item['@ID'] == id:
                wallets[item["Name"]] = item["Value"]
    return wallets

def main():
    print(scrapping())

if __name__=="__main__":
    main()
