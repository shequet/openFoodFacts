#! /usr/bin/env python3
# coding: utf-8
""" Terminal class """
from terminaltables import AsciiTable

from constant import OPENFOODFACTS_URL
from model.category import Category
from model.product import Product
from model.product_category import ProductCategory
from model.product_brand import ProductBrand
from model.product_store import ProductStore
from model.product_substitute import ProductSubstitute


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
            print("Veuillez entrer une valeur numérique !!!")

        print("1) Quel aliment souhaitez-vous remplacer ?")
        print("2) Retrouver mes aliments substitués.")

        choice_number = input()

        if choice_number == '1':
            self.product_choice(self.category_choice())
        elif choice_number == '2':
            print('a dev')
        else:
            self.first_choice(error=True)

    def category_choice(self, error=False):
        """ Categeries choices """

        categories = [[
            'Numéro',
            'Catégorie'
        ]]
        for category in self.category.show():
            categories.append([
                category[0],
                category[1]])

        print(AsciiTable(categories).table)

        if error:
            print("Veuillez entrer une valeur numérique !!!")
        print("Sélectionnez une catégorie:")

        category_id = input()

        if category_id.isdigit():
            return category_id
        else:
            self.category_choice(error=True)

    def product_choice(self, category_id, error=False):
        """ Products choices"""

        products = [[
            'Id',
            'Nutri Score',
            'Nom du produit']]

        for product in self.product.search_by_category(category_id):
            products.append([
                product[0],
                self.product.decode_nutriscore(int(product[5])),
                '{name} {quantity}'.format(name=product[2], quantity=product[4])
            ])

        print(AsciiTable(products).table)

        if error:
            print("Veuillez entrer une valeur numérique !!!")
        print("Sélectionnez un aliment:")
        product_id = input()

        if product_id.isdigit():
            self.substitute(product_id, category_id)
        else:
            self.product_choice(category_id, error=True)

    def substitute(self, product_id, category_id):
        """ Subtitute show"""

        products = [[
            'Type',
            'Id',
            'Nutri Score',
            'Marque(s)',
            'Nom du produit',
            'Boutique(s)',
            'lien OpenFoodFacts']]
        product = self.product.search_by_id(product_id)

        products.append([
            'Votre produit :',
            product['id'],
            product['nutriscore_letter'],
            ', '.join([' '.join(brands) for brands in self.product_brand.search_by_product(product_id)]),
            product['name'],
            ', '.join([' '.join(stores) for stores in self.product_store.search_by_product(product_id)]),
            '{url}/produit/{code}'.format(url=OPENFOODFACTS_URL, code=product['code'])])

        substitute_product = self.product.search_by_category_best_nutri_score(category_id, product['nutriscore'])

        if substitute_product is not None:
            products.append([
                'Produit de substitution :',
                substitute_product['id'],
                substitute_product['nutriscore_letter'],
                ', '.join([' '.join(brands) for brands in self.product_brand.search_by_product(substitute_product['id'])]),
                substitute_product['name'],
                ', '.join([' '.join(stores) for stores in self.product_store.search_by_product(substitute_product['id'])]),
                '{url}/produit/{code}'.format(url=OPENFOODFACTS_URL, code=substitute_product['code'])])
        else:
            products.append([
                'Produit de substitution :',
                '-',
                '-',
                '-',
                'Aucun produit trouvé',
                '-',
                '-'
            ])

        print(AsciiTable(products).table)

        print('Voulez-vous enregistrer le substitut ?\n1) Enregsitrer\n*) Autre touche retour au menu de départ')
        choice = input()

        if choice == '1':
            self.substitute_save(product_id, substitute_product['id'])
        self.first_choice()

    def substitute_save(self, product_id, substitute_product_id):
        """ Substitute Save"""

        self.product_substitute.add(product_id, substitute_product_id)
