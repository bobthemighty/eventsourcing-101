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


class BasketCreated(NamedTuple):
    basket_id: uuid.UUID


class Basket(Aggregate):

    def __init__(self, events=None):
        self.id = "EMPTY"
        super().__init__(events)

    # Deciders

    # Appliers

    # View methods

    def __str__(self):
        return print_basket(self)

    # Data Access
