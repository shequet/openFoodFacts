#! /usr/bin/env python3
# coding: utf-8
""" product Brand class """
from model.database import Database


class ProductBrand(Database):
    """ product Brand class"""

    def __init__(self):
        super().__init__()

    def add(self, product_id, brand_id):
        """ Add product brand"""

        if self.search_by_product_brand(product_id, brand_id) is None:
            self.execute("""
            INSERT INTO
                product_brands(
                    product_id,
                    brand_id) VALUES (
                    %s,
                    %s)
            """, (product_id, brand_id, ))

    def search_by_product_brand(self, product_id, brand_id):
        """ Search product brands by product id and brand id"""

        return self.fetch_one("""
        SELECT
            *
        FROM
            product_brands
        WHERE
            product_id=%s
        AND
            brand_id=%s;
        """, (product_id, brand_id))

    def search_by_product(self, product_id):
        """ Search product brands by product id"""

        return self.fetch_all("""
        SELECT
            b.name
        FROM
            product_brands as pb
        INNER JOIN
            brands as b On b.id = pb.brand_id
        WHERE
            pb.product_id=%s;
        """, (product_id, ))