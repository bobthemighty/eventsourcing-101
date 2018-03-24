# flake8: NOQA
# pylint: disable=unused-import
import uuid
from collections import Counter
from typing import NamedTuple

from pymongo import MongoClient

from mongobasket.aggregate import Aggregate, applies
from mongobasket import events

from .util import print_basket

client = MongoClient()
db = client.basket_db


class Basket(Aggregate):

    def __init__(self, events=None):
        self.id = "EMPTY"
        super().__init__(events)

    # Deciders

    @classmethod
    def create(cls, basket_id):
        basket = Basket()
        basket.raise_event(events.BasketCreated(basket_id))
        return basket

    def add_item(self, product, qty):
        self.raise_event(events.ItemAdded(self.id, product, qty))

    def remove(self, product):
        if product not in self.items:
            raise KeyError()
        self.raise_event(events.ItemRemoved(self.id, product))

    # Appliers

    @applies(events.BasketCreated)
    def on_created(self, event):
        self.id = event.basket_id
        self.items = Counter()

    @applies(events.ItemAdded)
    def on_added(self, event):
        self.items[event.product] += event.qty

    @applies(events.ItemRemoved)
    def on_removed(self, event):
        del self.items[event.product]

    # View methods

    def __str__(self):
        return print_basket(self)

    def is_empty(self):
        return not any(self.items)

    def get_item(self, product):
        return self.items[product]

    # Data Access

    def save(self):
        formatted_events = []
        for e in self.new_events:
            formatted_events.append(events.to_json(e))
        db.baskets.insert(formatted_events)
        self.new_events.clear()

    @classmethod
    def get(cls, basket_id):
        data = db.baskets.find({'basket_id': basket_id})
        read_events = []
        for json in data:
            read_events.append(events.from_json(json))
        return Basket(read_events)
