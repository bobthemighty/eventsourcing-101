This repo contains the code samples and slides for my "Eventsouring 101" talk.

There's a practice video of me mumbling and fumbling through it on [Youtube](https://www.youtube.com/watch?v=0l8vuYaaBU)

The master branch contains a simple shopping basket, with tests, that stores state in a mongo database.
The "from_scratch" branch has the code in a state ready for the live code exercise.

You'll need Docker and Python 3.6 in a virtual environment. To install things, run `make setup`

To run the tests, just run `make` or `make tests`
To start mongo, do `make mongo` and to view the slides, run `make serve` and then visit localhost:8000 in a browser.


Once you run `make setup` you can use the CLI tool to interact with shopping baskets:

```console
bob@localhost:~/code/talks/eventsourcing-101|master 
⇒  basket create socks
Created basket with id '5ab69073421aa917e62b4734'

bob@localhost:~/code/talks/eventsourcing-101|master 
⇒  basket add 5ab69073421aa917e62b4734 rocks

bob@localhost:~/code/talks/eventsourcing-101|master 
⇒  basket add 5ab69073421aa917e62b4734 clocks

bob@localhost:~/code/talks/eventsourcing-101|master 
⇒  basket remove 5ab69073421aa917e62b4734 socks 

bob@localhost:~/code/talks/eventsourcing-101|master 
⇒  basket get 5ab69073421aa917e62b4734

rocks = 1
clocks = 1
```

If you fancy completing this for yourself, you should just need to checkout the `from_scratch` branch and make all the tests pass.

You'll also need to implement the following _untested_ methods on the Basket class:

```python
def save(self):
   formatted_events = []
   for e in self.new_events:
       formatted_events.append(events.to_json(e))
   db.baskets.insert(formatted_events)
   
@classmethod
def get(cls, basket_id):
    read_events = []
    data = db.baskets.find({'basket_id': basket_id})
    for json in data:
        read_events.append(events.from_json(json))
        
    return Basket(read_events)
```

The cli tool should then work on the from_scratch branch, too.
