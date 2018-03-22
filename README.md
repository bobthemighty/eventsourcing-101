This repo contains the code smaples and slides for my "Eventsouring 101" talk.

The master branch contains a simple shopping basket, with tests, that stores state in a mongo database.
The "from_scratch" branch has the code in a state ready for the live code exercise.
The "eventsourced" branch is a less didactic, more fully fledged implementation.


To run the tests, just run `make` or `make tests`
To start mongo, do `make mongo` and to view the slides, run `make serve` and then visit localhost:8000 in a browser.