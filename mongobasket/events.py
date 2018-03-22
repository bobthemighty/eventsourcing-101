import uuid
from typing import NamedTuple


class BasketCreated(NamedTuple):
    basket_id: uuid.UUID


def from_json(event):
    name = event.pop('__event_name')
    del event['_id']
    cls_ = globals()[name]
    return cls_(**event)


def to_json(event):
    data = event._asdict()
    data['__event_name'] = event.__class__.__name__
    return data
