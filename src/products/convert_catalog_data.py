# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

'''
Utility script that can be run locally to convert the catalog data from a CSV file.

Usage:

python convert_catalog_data.py [-h] CATALOG_CSV_FILE

Where:
CATALOG_CSV_FILE is a CSV file with catalog data
'''

import argparse
import csv
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

    parser = argparse.ArgumentParser(description='Convert catalog data from CSV file.')
    parser.add_argument('file', metavar='CATALOG_CSV_FILE', type=open, help='CSV file with catalog data')
    args = parser.parse_args()
    
    products_yaml = open('src/products-service/data/products.yaml', 'w')
    categories_yaml = open('src/products-service/data/categories.yaml', 'w')

    reader = csv.DictReader(args.file)
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
