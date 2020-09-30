#! /usr/bin/env python3
# coding: utf-8
""" product Category class """
from app.database import Database


class ProductCategory(Database):
    """ product Category class"""

    def __init__(self):
        super().__init__()

    def add(self, product_id, category_id):
        """ Add product category"""

        if self.search_by_product_category(product_id, category_id) is None:
            self.execute("""
            INSERT INTO
                product_categories(
                    product_id,
                    category_id
                ) VALUES (
                    %s,
                    %s)
            """, (product_id, category_id, ))

    def search_by_product_category(self, product_id, category_id):
        """ Search product categories by product id and category id"""

        return self.fetch_one("""
        SELECT
            *
        FROM
            product_categories
        WHERE
            product_id=%s
        AND
            category_id=%s;
        """, (product_id, category_id))

    def search_by_product(self, product_id):
        """ Search product categories by product id"""

        return self.fetch_all("""
        SELECT
            c.name
        FROM
            product_categories as pc
        INNER JOIN
            categories as c On c.id = pc.category_id
        WHERE
            pc.product_id=%s;
        """, (product_id, ))
