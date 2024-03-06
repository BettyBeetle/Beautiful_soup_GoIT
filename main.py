import json
from connect import connect_to_mongodb, config
from scraper import parse_data


def save_json(quotes_data, authors_data):
    with open('quotes.json', 'w') as json_file:
        json.dump(quotes_data, json_file, indent=2) 

    with open('authors.json', 'w') as json_file:
        json.dump(authors_data, json_file, indent=2)

def upload_to_mongodb(quotes_data, authors_data):
    db = connect_to_mongodb()

    if db is not None:
        quotes_collection = db[config.get('DB', 'quotes_collection')]
        authors_collection = db[config.get('DB', 'authors_collection')]

        quotes_collection.insert_many(quotes_data)
        authors_collection.insert_many(authors_data)
        print("Dane zostały zapisane do kolekcji w bazie danych MongoDB Atlas.")
    else:
        print("Nie udało się połączyć z bazą danych MongoDB Atlas.")

if __name__ == '__main__':
    quotes_data, authors_data = parse_data()
    save_json(quotes_data, authors_data)
    upload_to_mongodb(quotes_data, authors_data)

    print("Dane zostały zapisane do bazy danych MongoDB Atlas.")


