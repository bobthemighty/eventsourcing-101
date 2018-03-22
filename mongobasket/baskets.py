from collections import Counter
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient()
db = client.basket_db


class Basket:

    def __init__(self, basket_id=None, items=None):
        self.__values = Counter(items)
        self.id = basket_id

    def add_item(self, product, qty=1):
        self.__values[product] += qty

    def remove(self, product):
        if not product in self.__values:
            raise KeyError(product)
        del self.__values[product]

    def __getitem__(self, product):
        return self.__values[product]

    def is_empty(self):
        return not any(self.__values)

    def save(self):
        data = dict(self.__values)

        if not self.id:
            _id = ObjectId()
            data['_id'] = _id
            db.baskets.insert_one(data)
            self.id = _id

        else:
            data['_id'] = self.id
            db.baskets.update({"_id": self.id}, data)

    @classmethod
    def get(cls, basket_id):
        _id = ObjectId(basket_id)
        data = db.baskets.find_one(_id)
        del data ['_id']
        return cls(basket_id=_id, items=data)

    def __str__(self):
        return "\n".join((
            f"{product} = {qty}"
            for product, qty in self.__values.items()
        ))
