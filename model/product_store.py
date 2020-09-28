#! /usr/bin/env python3
# coding: utf-8
""" product Store class """
from model.database import Database


class ProductStore(Database):
    """ product Store class"""

    def __init__(self):
        super().__init__()

    def add(self, product_id, store_id):
        """ Add product stores """

        if self.search_by_product_store(product_id, store_id) is None:
            self.execute("""
            INSERT INTO
                product_stores(
                    product_id,
                    store_id
                ) VALUES (
                    %s,
                    %s)
            """, (product_id, store_id, ))

    def search_by_product_store(self, product_id, store_id):
        """ Search product stores by product id and store id"""

        return self.fetch_one("""
        SELECT
            *
        FROM
            product_stores
        WHERE
            product_id=%s
        AND
            store_id=%s
        """, (product_id, store_id))

    def search_by_product(self, product_id):
        """ Search product store by product id"""

        return self.fetch_all("""
        SELECT
            s.name
        FROM
            product_stores as ps
        INNER JOIN
            stores as s ON s.id = ps.store_id
        WHERE
            ps.product_id=%s;
        """, (product_id, ))
