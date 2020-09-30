#! /usr/bin/env python3
# coding: utf-8
""" OpenFoodFacts class """
import requests

from constant import OPENFOODFACTS_URL,\
    OPENFOODFACTS_CATEGORIES,\
    OPENFOODFACTS_PAGE_SIZE
from app.database import Database
from app.model.product import Product
from app.model.brand import Brand


class OpenFoodFacts:
    """ OpenFoodFacts class """

    def __init__(self):
        self.url = OPENFOODFACTS_URL

    def import_products(self):
        """ Import all products in database"""

        db_product = Product()

        for category in OPENFOODFACTS_CATEGORIES:
            products = self.call_api('{url}/categorie/{category}.json'.format(
                url=self.url,
                category=category))

            for product in products:
                if 'product_name_fr' in product \
                        and product['product_name_fr'] != ""\
                        and product['code'] != ""\
                        and 'nutriscore_score' in product\
                        and product['nutriscore_score'] != "":
                    db_product.add(
                        name=product['product_name_fr'],
                        link=product['link'] if 'link' in product and product['link'] != "" else None,
                        stores=product['stores'] if 'stores' in product else None,
                        brands=product['brands'] if 'brands' in product else None,
                        categories=product['categories'] if 'categories' in product else None,
                        code=product['code'],
                        quantity=product['quantity'] if 'quantity' in product else None,
                        nutriscore=product['nutriscore_score'] if 'nutriscore_score' in product else None,
                    )

    def call_api(self, url, page=1, products=[]):
        """ Call Api open food facts"""

        r = requests.get(
            url,
            params={
                'page': page,
                'page_size': OPENFOODFACTS_PAGE_SIZE
            })
        if r.status_code == 200 and r.json is not None:
            data = r.json()
            if len(data['products']) > 0:
                products.extend(data['products'])
                print('--Page:[{page}]--Total products:[{products}]--'.format(
                    page=page,
                    products=len(products)))
                return self.call_api(
                    url=url,
                    page=int(data['page']) + 1,
                    products=products)

        return products
