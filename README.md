Flask Heroku Sample
====================

This is a series of scripts that:

- builds an NMF topic model (cprop.py)
- listens to a tweet stream on selected keywords identifying similiar tweets by topic (streamer.py)
- displays selected tweets in an infinite scroll (app.py and templates dir)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

View here: [https://www.cprop.tech/](https://www.cprop.tech/)

## Development Setup

* `pipenv install`

* `pipenv shell`

* `python app.py`

## Deploy

* `heroku create`

* `heroku addons:create heroku-postgresql:hobby-dev`

* `git push heroku master`

* Note: make sure you run `db.create_all()` to create the tables.
