import requests
import json
from parsel import Selector

def parse(url: str) -> list[dict]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    with open('books2.html', 'w', encoding='utf-8') as file:
        file.write(response.text)

    with open('books2.html', 'r') as file:
        html = file.read()

    selector = Selector(html)
    data = []

    books = selector.css('article.product_pod')
    for book in books:
        title = book.css('h3 a::attr(title)').get()
        image = book.css('img::attr(src)').get()
        link = book.css('a::attr(href)').get()
        rating = book.css('p.star-grating::attr(class)').get().split()[-1] if book.css('p.star-rating::attr(class)').get() else None
        price = book.css('.price_color::text').get()
        stock = book.css('.instock.availability::text').get()
        position = books.index(book) + 1

        data.append({
            'title': title,
            'image': image,
            'price': price,
            'stock': stock,
            'link': link,
            'rating': rating,
            'position': position
        })

    return data

result = parse(url='https://books.toscrape.com/')
print(json.dumps(result, indent=2, ensure_ascii=False))
