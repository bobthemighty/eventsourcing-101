# pylint: disable=attribute-defined-outside-init
import uuid

from mongobasket.baskets import Basket
from mongobasket import events

class BasketTest:

    BASKET_ID = uuid.uuid4()

    @property
    def event(self):
        assert len(self.basket.new_events) == 1, "Should have one new event"
        return self.basket.new_events[0]

    def has_event(self, cls):
        return isinstance(self.event, cls)

    def raised_no_events(self):
        return not any(self.basket.new_events)


class When_creating_a_new_basket(BasketTest):

    def because_we_create_a_basket(self):
        self.basket = Basket.create(self.BASKET_ID)

    def it_should_not_contain_any_products(self):
        assert self.basket.is_empty()

    def it_should_raise_basket_created(self):
        assert self.has_event(events.BasketCreated)
        assert self.event.basket_id == self.BASKET_ID

    def it_should_have_the_correct_basket_id(self):
        assert self.basket.id == self.BASKET_ID


#class When_adding_a_new_item(BasketTest):
#
#    def given_an_empty_basket(self):
#        self.basket = Basket([
#            events.BasketCreated(self.BASKET_ID)
#        ])
#
#    def because_we_add_a_product(self):
#        self.basket.add_item("coffee", qty=3)
#
#    def it_should_contain_the_product(self):
#        assert self.basket.get_item('coffee') == 3, "Should contain 3 coffees"
#
#    def it_should_raise_item_added(self):
#        assert isinstance(self.event, events.ItemAdded)
#        assert self.event.basket_id == self.BASKET_ID
#        assert self.event.product == "coffee"
#        assert self.event.qty == 3
#
#    def it_should_not_be_empty(self):
#        assert not self.basket.is_empty()
#
# data access nao plz
#
#
#
#
#class When_removing_a_product(BasketTest):
#
#    def given_a_basket(self):
#        self.basket = Basket([
#            events.BasketCreated(self.BASKET_ID),
#            events.ItemAdded(self.BASKET_ID, "apple", 2)
#        ])
#
#    def because_we_remove_an_item(self):
#        self.basket.remove("apple")
#
#    def it_should_empty_the_items(self):
#        assert self.basket.is_empty()
#
#    def it_should_raise_item_removed(self):
#        assert self.has_event(events.ItemRemoved)
#        assert self.event.basket_id == self.BASKET_ID
#        assert self.event.product == "apple"
#
#
#class When_removing_a_product_that_doesnt_exist(BasketTest):
#
#    def given_a_basket(self):
#        self.exn = None
#        self.basket = Basket([
#            events.BasketCreated(self.BASKET_ID),
#            events.ItemAdded(self.BASKET_ID, "apple", 1)
#        ])
#
#    def because_we_remove_an_item(self):
#        try:
#            self.basket.remove("sausages")
#        except Exception as e:
#            self.exn = e
#
#    def it_should_not_empty_the_items(self):
#        assert not self.basket.is_empty()
#
#    def it_should_raise_a_key_error(self):
#        assert isinstance(self.exn, KeyError)
#
#    def it_should_not_raise_any_events(self):
#        assert self.raised_no_events()
