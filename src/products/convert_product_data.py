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
    product['image'] = product['id'] + ".jpg"
    return product

def create_category(id, product):
    return {
        'id': id,
        'name': product['category'],
        'image': product['image']
    }


if __name__=="__main__":
    beers_csv = open('beers.csv', 'r')
    products_yaml = open('src/products-service/data/products.yaml', 'w')
    categories_yaml = open('src/products-service/data/categories.yaml', 'w')

    reader = csv.DictReader(beers_csv)
    products = list(reader)
    categories = []
    category_names = set()

    for product in products:
        product = format_product(product)
        if product['category'] not in category_names:
            category_names.add(product['category'])
            categories.append(create_category(len(category_names), product))

    yaml.dump(products, products_yaml, allow_unicode=True, sort_keys=False)
    yaml.dump(categories, categories_yaml, allow_unicode=True, sort_keys=False)
