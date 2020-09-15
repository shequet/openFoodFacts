#! /usr/bin/env python3
# coding: utf-8
""" OpenFoodFacts project"""
from openfoodfact import OpenFoodFacts


def main():
    """ Main function """
    open_food_facts = OpenFoodFacts()
    open_food_facts.import_category('boissons')


if __name__ == "__main__":
    main()
