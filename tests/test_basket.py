import logging
import uuid
from collections import Counter
from typing import NamedTuple

from mongobasket.baskets import Basket


class When_creating_a_new_basket:

    def because_we_create_a_basket(self):
        self.basket = Basket()

    def it_should_not_contain_any_products(self):
        assert self.basket.is_empty()


class When_adding_a_new_item:

    def given_an_empty_basket(self):
        self.basket = Basket()

    def because_we_add_an_apple(self):
        self.basket.add_item("apple")

    def it_should_add_one_apple(self):
        assert self.basket['apple'] == 1

class When_adding_an_item_with_quantity:

    def given_an_empty_basket(self):
        self.basket = Basket()

    def because_we_add_an_apple(self):
        self.basket.add_item("apple", qty=3)

    def it_should_add_one_apple(self):
        assert self.basket['apple'] == 3


class When_adding_more_to_an_existing_product:

    def given_a_basket(self):
        self.basket = Basket()
        self.basket.add_item("apple", 2)

    def because_we_add_an_apple(self):
        self.basket.add_item("apple", qty=3)

    def it_should_add_to_the_quantity(self):
        assert self.basket['apple'] == 5


class When_removing_a_product:

    def given_a_basket(self):
        self.basket = Basket()
        self.basket.add_item("apple", 2)

    def because_we_remove_an_item(self):
        self.basket.remove("apple")

    def it_should_empty_the_items(self):
        assert self.basket.is_empty()


class When_removing_a_product_that_doesnt_exist:

    def given_a_basket(self):
        self.basket = Basket()
        self.basket.add_item("apple")

    def because_we_remove_an_item(self):
        try:
            self.basket.remove("sausages")
        except Exception as e:
            self.exn = e

    def it_should_not_empty_the_items(self):
        assert not self.basket.is_empty()

    def it_should_raise_a_key_error(self):
        assert isinstance(self.exn, KeyError)
