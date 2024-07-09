import requests
from bs4 import BeautifulSoup
import json

class EbayProductScraper:
    def __init__(self, url):
        self.url = url
        self.soup = self._get_soup()

    def _get_soup(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')
        else:
            raise Exception(f"Failed to retrieve content from {self.url}")

    def get_product_name(self):
        name = self.soup.find('h1', {'class': 'x-item-title__mainTitle'})
        return name.text.strip() if name else None

    def get_product_image(self):
        image_container = self.soup.find('div', {'class': 'ux-image-carousel-container image-container'})
        image_links = []
        if image_container:
            images = image_container.find_all('img')
            for image in images:
                src = image.get('data-src')
                if src:
                    image_links.append(src)
        return image_links if image_links else None

    def get_product_price(self):
        price = self.soup.find('div', {'class': 'x-price-primary'})
        return price.text.strip() if price else None

    def get_seller(self):
        seller = self.soup.find('div', {'class': 'x-sellercard-atf__info__about-seller'})
        return seller.text.strip() if seller else None

    def get_delivery_price(self):
        delivery = self.soup.find('div', {'class': 'ux-labels-values__values col-9'})
        return delivery.text.strip() if delivery else None

    def to_json(self):
        data = {
            'name': self.get_product_name(),
            'image_link': self.get_product_image(),
            'product_link': self.url,
            'price': self.get_product_price(),
            'seller': self.get_seller(),
            'delivery_price': self.get_delivery_price()
        }
        return json.dumps(data, indent=4)

    def save_to_file(self, filename):
        data = self.to_json()
        with open(filename, 'w') as f:
            f.write(data)

url = ""
scraper = EbayProductScraper(url)
print(scraper.to_json())
scraper.save_to_file('product_data.json')
