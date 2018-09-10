from peewee import *
from playhouse import shortcuts
from playhouse.sqlite_ext import JSONField
import os
from playhouse.shortcuts import model_to_dict, dict_to_model

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')
db = PostgresqlDatabase('d4gqaf7esuge89', dsn=DATABASE_URL)

class Tweet(Model):
    class Meta:
        database = db
    id                    = BigIntegerField(unique=True)
    retweet_count         = IntegerField()
    favorite_count        = IntegerField()
    reply_count           = IntegerField()
    text                  = CharField()
    category              = CharField()
    category_score        = FloatField()
    tweet_data            = JSONField()
    model_data            = JSONField()
    date                  = DateTimeField()
    def rollback(self):
        db.rollback()
    def from_dict(data):
        return shortcuts.dict_to_model(Tweet, data, ignore_unknown=True)
    def to_dict(data):
        return shortcuts.model_to_dict(data)


db.create_tables([Tweet])

if __name__ == "__main__":
    res = Tweet.select()
    ids = [Tweet.to_dict(sw)['id'] for sw in res]
    print(ids)
