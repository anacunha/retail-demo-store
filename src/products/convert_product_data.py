import csv
import uuid
import yaml

def format_product(product):
    product['abv'] = float(product['abv'])
    product['category'] = product['category'].replace(' ', '-').lower()
    if product['ibu'] == 'N/A':
        product.pop('ibu')
    else:
        product['ibu'] = int(product['ibu'])
    return product

if __name__=="__main__":
    beers_csv = open('beers.csv', 'r')
    products_yaml = open('src/products-service/data/products.yaml', 'w')
    categories_yaml = open('src/products-service/data/categories.yaml', 'w')

    reader = csv.DictReader(beers_csv)
    products = list(reader)
    category_names = set()

    for product in products:
        product = format_product(product)
        category_names.add(product['category'])

    yaml.dump(products, products_yaml, allow_unicode=True, sort_keys=False)

    categories = []
    for category_name in sorted(category_names):
        category = {
            'id': str(uuid.uuid4()),
            'name': category_name
        }
        categories.append(category)

    yaml.dump(categories, categories_yaml, allow_unicode=True, sort_keys=False)
