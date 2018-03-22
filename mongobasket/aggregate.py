import logging


def applies(event):
    """
    This decorator just adds a new field to the func object
    `_handles` which describes the event type handled by
    the func
    """

    def wrapper(func):
        func._applies = event

        return func

    return wrapper


class EventRegistry(type):
    """
    Extends the `type` metaclass to add an event registry to
    classes.

    When initialising a new class, we iterate the members of
    the class looking for a _handles property and add them
    to a dict so we can do event dispatch later.
    """

    def __new__(mcs, name, bases, namespace, **_):
        result = type.__new__(mcs, name, bases, dict(namespace))
        result._handlers = {
            value._applies: value

            for value in namespace.values() if hasattr(value, '_applies')
        }
        # Extend handlers with the values from the inheritance chain

        for base in bases:
            if (base._handlers):
                for handler in base._handlers:
                    result._handlers[handler] = base._handlers[handler]

        return result


class Aggregate(metaclass=EventRegistry):
    """
    Base class for event sourced aggregates
    """

    @classmethod
    def get_stream(cls, id):
        return cls.__name__.lower() + '-' + str(id)

    def __init__(self, events=None):
        self.events = events or []
        self.new_events = []
        self.replay()

    def replay(self):
        for e in self.events:
            self.apply(e)

    def apply(self, e):
        handler = self._handlers.get(type(e))

        if handler:
            handler(self, e)
        else:
            logging.warning("no handler found")

    def raise_event(self, e):
        self.events.append(e)
        self.new_events.append(e)
        self.apply(e)



