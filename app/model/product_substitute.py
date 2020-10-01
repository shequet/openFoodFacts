#! /usr/bin/env python3
# coding: utf-8
""" product Substitute class """
from app.database import Database


class ProductSubstitute(Database):
    """ product Substitute class"""

    def __init__(self):
        super().__init__()

    def add(self, product_id, substitute_product_id):
        """ Add product substitute"""

        if self.search(product_id, substitute_product_id) is None:
            self.execute("""
            INSERT INTO
                product_substitute(
                    product_id,
                    substitute_product_id
                ) VALUES (
                    %s,
                    %s)
            """, (product_id, substitute_product_id, ))

    def search(self, product_id, substitute_product_id):
        """ Search product substitute by product id and substitute product id"""

        return self.fetch_one("""
        SELECT
            *
        FROM
            product_substitute
        WHERE
            product_id=%s
        AND
            substitute_product_id=%s;
        """, (product_id, substitute_product_id))

    def select_all(self):
        """ Select all substitute"""

        return self.fetch_all("""
        SELECT
            ps.product_id,
            ps.substitute_product_id
        FROM
            product_substitute as ps""")
