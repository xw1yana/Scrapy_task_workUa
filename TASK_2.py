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

url = 'https://www.ebay.com/itm/364911055895?_trkparms=amclksrc%3DITM%26aid%3D1110006%26algo%3DHOMESPLICE.SIM%26ao%3D1%26asc%3D267025%26meid%3D64f606e9dee345eca1d66f78cab51e52%26pid%3D101875%26rk%3D3%26rkt%3D4%26sd%3D364911054207%26itm%3D364911055895%26pmt%3D1%26noa%3D0%26pg%3D2332490%26algv%3DSimplAMLv11WebTrimmedWithMfgPhase2WithCassiniVisualRankerAndBertRecallWithPLXSizeFilterCPCAutoManual%26brand%3DUnique&_trksid=p2332490.c101875.m1851&itmprp=cksum%3A36491105589564f606e9dee345eca1d66f78cab51e52%7Cenc%3AAQAJAAABUIc%252Fzndrrg02zuwb5ato5EUGq81aQnuuc6d%252BRM8Km2BzAE2pVFKK2H54K2ZN%252Bb2aIyUEBIii8NKFV1Qfe7yOziXcC3I5yb7ZxmkUxtDpURMf22jzuw2ZurJSTCMDqOKAgeIoi%252FxZni%252BHrnGFW5VE9zLZtbxleqRT%252F2A9pS9g4c0TXdiUHuAmia0kCQ5ZdP8ndfPOuMj%252FhzQZl7JX%252FJN5S3UdWNXc%252BAcsjfgJaJUwAmu8%252Byi%252Fd6CUAU%252BK%252B5fcAL0be7lNVIB5MVFmpObfTOt77HYtpxQ9bPb9NcvsI%252BZwCBncr3xisgRgVoYOf3ev9tLPs1kJZzeEQbh%252F7Dl9IriEDUqsTZQklMFP5ki00I1i4gzyHL3dp9Inmeyt%252FFTdGBGR7Bhxk%252FjQqJwQ9Hq8lWDen6mkngTttmTiMHRY6ACPC3cGk25tYKfwsIhUpyQnrGVsNQ%253D%253D%7Campid%3APL_CLK%7Cclp%3A2332490&itmmeta=01J2BMH7M63RK6WGJ80876K11E'
scraper = EbayProductScraper(url)
print(scraper.to_json())
scraper.save_to_file('product_data.json')