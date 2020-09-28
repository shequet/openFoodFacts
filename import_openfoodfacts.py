#! /usr/bin/env python3
# coding: utf-8
""" OpenFoodFacts project"""
from core.openfoodfact import OpenFoodFacts


def main():

    open_food_facts = OpenFoodFacts()
    open_food_facts.import_products()


if __name__ == "__main__":
    main()
