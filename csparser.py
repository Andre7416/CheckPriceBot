from bs4 import BeautifulSoup
import requests


class Parse:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
            }
        self.response = requests.get(url, headers=self.headers)
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def get_info(self):
        if self.url.find('https://www.farfetch.com/ru') != -1:
            title1 = self.soup.find('a', attrs={'data-tstid': 'cardInfo-title'})
            title2 = self.soup.find('span', attrs={'data-tstid': 'cardInfo-description'})
        else:
            title_block = self.soup.find('div', class_='item-info_345V6')
            if title_block:
                title1 = title_block.find('h1')
                title2 = title_block.find('h2')
            else:
                title1 = title_block
                title2 = title_block
        if not title1:
            title1 = 'товар не найден (возможно его нет в наличии)'
        else:
            title1 = title1.text
        if not title2:
            title2 = ''
        else:
            title2 = title2.text
        return title1.strip() + ' ' + title2.strip()

    def get_price(self):
        if self.url.find('https://www.farfetch.com/ru') != -1:
            sale_price = self.soup.find('strong', attrs={'data-tstid': 'priceInfo-onsale'})
            not_sale_price = self.soup.find('span', attrs={'data-tstid': 'priceInfo-original'})
        else:
            sale_price = self.soup.find('div', class_='MuiTitle4-title4 currentPrice_135Ct')
            not_sale_price = self.soup.find('span', class_='MuiBody1-body1 oldPrice_Nd18A')

        ans = 1e12

        if not_sale_price:
            not_sale_price = not_sale_price.text
            not_sale_price = not_sale_price.strip().replace('\xa0', '').replace('₽', '')
            not_sale_price = not_sale_price.replace(',', '').replace(' ', '').replace('руб', '')
            not_sale_price = int(not_sale_price)
            ans = not_sale_price

        if sale_price:
            sale_price = sale_price.text
            sale_price = sale_price.strip().replace('\xa0', '').replace('₽', '')
            sale_price = sale_price.replace(',', '').replace(' ', '').replace('руб', '')
            sale_price = int(sale_price)
            ans = sale_price

        return ans
