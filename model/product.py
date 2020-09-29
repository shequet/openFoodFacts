#! /usr/bin/env python3
# coding: utf-8
""" Product class """
from model.database import Database
from model.category import Category
from model.product_category import ProductCategory
from model.brand import Brand
from model.store import Store
from model.product_brand import ProductBrand
from model.product_store import ProductStore
from model.product_substitute import ProductSubstitute
from constant import LIMIT_PRODUCT_ITEMS


class Product(Database):
    """ Product class"""

    def __init__(self):
        super().__init__()
        self.category = Category()
        self.product_category = ProductCategory()
        self.brand = Brand()
        self.store = Store()
        self.product_brand = ProductBrand()
        self.product_store = ProductStore()
        self.product_substitute = ProductSubstitute()

    def add(self,
            name,
            link,
            quantity,
            categories,
            code,
            stores,
            brands,
            nutriscore):
        """ Add product"""

        product = self.search_by_code(code)
        if product is None:
            self.execute("""
            INSERT INTO
                products(
                    name,
                    link,
                    code,
                    quantity,
                    nutriscore
                    ) VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s)
            """, (name, link, code, quantity, nutriscore))
            product = self.search_by_code(code)

        for category in categories.split(','):
            category_id = self.category.add(category.strip())
            self.product_category.add(product[0], category_id)

        if brands is not None:
            for brand in brands.split(','):
                brand_id = self.brand.add(brand.strip())
                self.product_brand.add(product[0], brand_id)

        if stores is not None:
            for store in stores.split(','):
                store_id = self.store.add(store.strip())
                self.product_store.add(product[0], store_id)

    def search_by_code(self, code):
        """ Search product by code"""

        return self.fetch_one("""
        SELECT
            *
        FROM
            products
        WHERE
            code=%s;
        """, (code, ))

    def search_by_category(self, category_id):
        """ Search all products by category """

        return self.fetch_all("""
        SELECT
            p.id,
            p.code,
            p.name,
            p.link,
            p.quantity,
            p.nutriscore
        FROM
            products as p
        INNER JOIN
            product_categories as pc ON pc.product_id = p.id
        WHERE
            pc.category_id=%s
        LIMIT {limit};
        """.format(limit=LIMIT_PRODUCT_ITEMS), (category_id, ))

    def search_by_category_best_nutri_score(self, category_id, nutri_score):
        """ Look for the product that has
        the best nutriscore in its category """

        product = self.fetch_one("""
            SELECT
                p.id,
                p.code,
                p.name,
                p.link,
                p.quantity,
                p.nutriscore
            FROM
                products as p
            INNER JOIN
                product_categories as pc ON pc.product_id = p.id
            WHERE
                pc.category_id=%s
            AND
                p.nutriscore < %s
            AND
                p.nutriscore >= 0
            ORDER BY
                p.nutriscore ASC
            LIMIT 1;
            """, (category_id, nutri_score))

        if product:
            return {
                'id': product[0],
                'code': product[1],
                'name': product[2],
                'link': product[3],
                'quantity': product[4],
                'nutriscore': product[5],
                'nutriscore_letter': self.decode_nutriscore(int(product[5]))
            }
        return None

    def search_by_id(self, id):
        """ Search product by id """

        product = self.fetch_one("""
            SELECT
                id,
                code,
                name,
                link,
                quantity,
                nutriscore
            FROM
                products
            WHERE
                id=%s;
            """, (id, ))

        if product:
            return {
                'id': product[0],
                'code': product[1],
                'name': product[2],
                'link': product[3],
                'quantity': product[4],
                'nutriscore': product[5],
                'nutriscore_letter': self.decode_nutriscore(int(product[5]))
            }

    def decode_nutriscore(self, nutri_score):
        """ Decode nutriscore """

        if nutri_score < -1:
            return 'A'
        elif 0 <= nutri_score <= 2:
            return 'B'
        elif 3 <= nutri_score <= 10:
            return 'C'
        elif 11 <= nutri_score <= 18:
            return 'D'
        elif nutri_score >= 19:
            return 'E'
        else:
            return None
