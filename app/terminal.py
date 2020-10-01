#! /usr/bin/env python3
# coding: utf-8
""" Terminal class """
from terminaltables import AsciiTable

from constant import OPENFOODFACTS_URL
from app.model.category import Category
from app.model.product import Product
from app.model.product_category import ProductCategory
from app.model.product_brand import ProductBrand
from app.model.product_store import ProductStore
from app.model.product_substitute import ProductSubstitute


class Terminal:
    """ Terminal class """

    def __init__(self):
        self.category = Category()
        self.product = Product()
        self.product_category = ProductCategory()
        self.product_brand = ProductBrand()
        self.product_store = ProductStore()
        self.product_substitute = ProductSubstitute()
        self.first_choice()

    def first_choice(self, error=False):
        """ First choice"""

        if error:
            print("Please enter a valid numeric value !!!")

        print("1) What food do you want to replace ?")
        print("2) Find my substitute foods.")

        choice_number = input()

        if choice_number == '1':
            self.product_choice(self.category_choice())
        elif choice_number == '2':
            self.substitute_choice()
        else:
            self.first_choice(error=True)

    def category_choice(self, error=False):
        """ Categeries choices """

        categories = [[
            'Number',
            'Category'
        ]]
        for category in self.category.show():
            categories.append([
                category[0],
                category[1]])

        print(AsciiTable(categories).table)

        if error:
            print("Please enter a valid numeric value !!!")
        print("Select a category:")

        category_id = input()

        if category_id.isdigit():
            return category_id
        else:
            self.category_choice(error=True)

    def product_choice(self, category_id, error=False):
        """ Products choices"""

        categories = self.product.search_by_category(category_id)

        if len(categories) == 0:
            self.product_choice(self.category_choice())

        products = [[
            'Id',
            'Nutri Score',
            'Product Name']]

        for product in categories:
            products.append([
                product[0],
                self.product.decode_nutriscore(int(product[5])),
                '{name} {quantity}'.format(
                    name=product[2],
                    quantity=product[4]
                )
            ])

        print(AsciiTable(products).table)

        if error:
            print("Please enter a valid numeric value !!!")
        print("Select a food:")
        product_id = input()

        if product_id.isdigit():
            self.substitute(product_id, category_id)
        else:
            self.product_choice(category_id, error=True)

    def substitute(self, product_id, category_id):
        """ Subtitute show"""

        product = self.product.search_by_id(product_id)

        if product is None:
            self.product_choice(category_id=category_id, error=True)

        product_brands = self.product_brand.search_by_product(product_id)
        product_stores = self.product_store.search_by_product(product_id)
        products = [[
            'Type',
            'Id',
            'Nutri Score',
            'Brand(s)',
            'Product Name',
            'Shop(s)',
            'OpenFoodFacts Link'], [
            'Your product :',
            product['id'],
            product['nutriscore_letter'],
            ', '.join([' '.join(brands) for brands in product_brands]),
            product['name'],
            ', '.join([' '.join(stores) for stores in product_stores]),
            '{url}/produit/{code}'.format(
                url=OPENFOODFACTS_URL,
                code=product['code']
            )]]

        substitute_product = self.product.search_by_category_best_nutri_score(
            category_id=category_id,
            nutri_score=product['nutriscore']
        )
        substitute_brands = self.product_brand.search_by_product(
            product_id=substitute_product['id']
        )
        substitute_stores = self.product_store.search_by_product(
            product_id=substitute_product['id']
        )
        if substitute_product is not None:
            products.append([
                'Substitution product :',
                substitute_product['id'],
                substitute_product['nutriscore_letter'],
                ', '.join(
                    [' '.join(brands) for brands in substitute_brands]),
                substitute_product['name'],
                ', '.join(
                    [' '.join(stores) for stores in substitute_stores]),
                '{url}/produit/{code}'.format(
                    url=OPENFOODFACTS_URL,
                    code=substitute_product['code']
                )])
        else:
            products.append([
                'Substitution product :',
                '-',
                '-',
                '-',
                'No product found',
                '-',
                '-'
            ])

        print(AsciiTable(products).table)

        print('Do you want to save the substitute ?')
        print('1) Save')
        print('*) Other key back to the start menu')
        choice = input()

        if choice == '1':
            self.product_substitute.add(
                product_id=product_id,
                substitute_product_id=substitute_product['id'])
        self.first_choice()

    def substitute_choice(self):
        """ Substitute choice"""

        for product_substitute in self.product_substitute.select_all():
            products = [[
                'Type',
                'Id',
                'Nutri Score',
                'Brand(s)',
                'Product Name',
                'Shop(s)',
                'OpenFoodFacts Link']]

            product_id = product_substitute[0]
            substitute_id = product_substitute[1]

            product = self.product.search_by_id(product_id)
            substitute = self.product.search_by_id(substitute_id)

            product_brands = self.product_brand.search_by_product(product_id)
            product_stores = self.product_store.search_by_product(product_id)
            products.append([
                'Your product :',
                product['id'],
                product['nutriscore_letter'],
                ', '.join([' '.join(brands) for brands in product_brands]),
                product['name'],
                ', '.join([' '.join(stores) for stores in product_stores]),
                '{url}/produit/{code}'.format(
                    url=OPENFOODFACTS_URL,
                    code=product['code']
                )])

            substitute_brands = self.product_brand.search_by_product(
                product_id=substitute_id
            )
            substitute_stores = self.product_store.search_by_product(
                product_id=substitute_id
            )
            products.append([
                'Substitution product :',
                substitute['id'],
                substitute['nutriscore_letter'],
                ', '.join([' '.join(brands) for brands in substitute_brands]),
                substitute['name'],
                ', '.join([' '.join(stores) for stores in substitute_stores]),
                '{url}/produit/{code}'.format(
                    url=OPENFOODFACTS_URL,
                    code=substitute['code']
                )])

            print(AsciiTable(products).table)
        self.first_choice()
