import requests
import lxml.html
import json

response = requests.get('https://www.chitai-gorod.ru/catalog/books/')
tree = lxml.html.fromstring(response.text)

for category in tree.xpath('//div/div/div/div/ul/li/a'):
    print(category.text, category.get('href'))
    response = requests.get('https://www.chitai-gorod.ru' + category.get('href'))
    tree = lxml.html.fromstring(response.text)

    for name_of_the_book_page1 in tree.xpath('//div/a[@class="product-card__link js-watch-productlink"]'):
        print(name_of_the_book_page1.text_content(), name_of_the_book_page1.get('href'))
        response = requests.get('https://www.chitai-gorod.ru' + name_of_the_book_page1.get('href'))
        tree = lxml.html.fromstring(response.text)

        rating = tree.xpath('//div/span[@class="js__rating_count"]')
        print(rating[0].text)
        price = tree.xpath('//div/div[@class="price"]')
        print(price[0].text)
        description = tree.xpath('//div/div[@itemprop="description"]')
        print(description[0].text)

        result1 = {'name_category': category.text, 'book': name_of_the_book_page1.text_content(),
          'description': description[0].text, 'price': price[0].text, 'rating': rating[0].text}

        with open("books.txt", "a", encoding='utf-8') as file:
            file.write(f'{json.dumps(result1, ensure_ascii=False)}\n')

    for page in tree.xpath('//a[@class="pagination-item"]'):
        print(page.text, page.get('href'))
        response = requests.get('https://www.chitai-gorod.ru' + page.get('href'))
        tree = lxml.html.fromstring(response.text)

        for name_of_the_book in tree.xpath('//div/a[@class="product-card__link js-watch-productlink"]'):
            print(name_of_the_book.text_content(), name_of_the_book.get('href'))

            result = {'name_category': category.text, 'book': name_of_the_book.text_content(),
                      'description': None, 'price': None, 'rating': None}

            if rating:
                result['rating'] = rating = tree.xpath('//div/span[@class="js__rating_count"]')
            if price:
                result['price'] = price = tree.xpath('//div/div[@class="price"]')
            if description:
                result['description'] = description = tree.xpath('//div/div[@itemprop="description"]')

            with open("books.txt", "a", encoding='utf-8') as file:
                file.write(f'{json.dumps(result, ensure_ascii=False)}\n')
