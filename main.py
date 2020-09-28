#! /usr/bin/env python3
# coding: utf-8
""" OpenFoodFacts project"""
from terminaltables import AsciiTable

from core.terminal import Terminal


def main():
    """ Main function """

    terminal = Terminal()
    terminal.first_choice()


if __name__ == "__main__":
    main()
