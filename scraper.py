import requests
from bs4 import BeautifulSoup
import unicodedata
from http import HTTPStatus



quotes_data = []
authors_data = []

url = 'https://quotes.toscrape.com'


def parse_data():
    page_no = 1
    while True:
        response = requests.get(f"{url}/page/{page_no}")
        if response.status_code == HTTPStatus.OK:
            soup = BeautifulSoup(response.text, 'html.parser')
            quotes = soup.find_all('div', class_='quote')
            if quotes:
                for quote in quotes:
                    tags = [tag.text for tag in quote.find_all('a', class_='tag')]
                    author_name = quote.find('small', class_='author').text.strip()
                    quote_text = quote.find('span', class_='text').text.strip()
                    
                    quote_text = unicodedata.normalize('NFKD', quote_text).encode('ascii', 'ignore').decode('utf-8')
                    author_name = unicodedata.normalize('NFKD', author_name).encode('ascii', 'ignore').decode('utf-8')
                    author_url = url + quote.find("a")["href"]
                    
                    quotes_data.append({
                        "tags": tags,
                        "author": author_name,
                        "quote": quote_text
                    })
                   

                    author_response = requests.get(author_url)
                    if author_response.status_code == HTTPStatus.OK:          
                        author_soup = BeautifulSoup(author_response.text, 'html.parser')

                        birth_date = author_soup.find("span", class_='author-born-date').get_text()
                        birth_place = author_soup.find("span", class_='author-born-location').get_text()
                        author_descriptions = author_soup.find("div", class_='author-description').get_text().strip()
                        author_descriptions = unicodedata.normalize('NFKD', author_descriptions).encode('ascii', 'ignore').decode('utf-8')
                        birth_place = unicodedata.normalize('NFKD', birth_place).encode('ascii', 'ignore').decode('utf-8')

                        author_data =({
                            "fullname": author_name,
                            "born_date": birth_date,
                            "born_location": birth_place,
                            "description": author_descriptions
                        })

                        if author_data not in authors_data:
                            authors_data.append(author_data)
                    else:
                        print("Error fetching author details")
                page_no += 1
            else:
                break
        else:
            print("Error fetching page:", response.status_code)
            break
    return quotes_data, authors_data    
