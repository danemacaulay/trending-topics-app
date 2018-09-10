from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from db import Tweet
import pydash
import cprop

class StdOutListener(StreamListener):

    def __init__(self):
        model, vectorizer = cprop.load_model()
        self.model = model
        self.vectorizer = vectorizer

    def should_reject(self, data):
        if 'lang' not in data:
            return True
        if data['lang'] != 'en':
            return True
        if 'retweeted_status' not in data:
            return True
        if data['retweeted_status']['retweet_count'] < 100:
            return True
        return False

    def should_reject_by_topic(self, score, category_id):
        if score < 0.15:
            return True
        if category_id in [1, 2, 4, 6]:
            return True

    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        data = json.loads(data)
        if self.should_reject(data):
            return True
        retweet_data = data['retweeted_status']
        annotated_data = cprop.annotate_data([retweet_data['text']],
                                             self.model,
                                             self.vectorizer)
        category = pydash.get(annotated_data, 'top_cat.0')
        category_id = pydash.get(annotated_data, 'top_cat_id.0')
        score = pydash.get(annotated_data, 'scores.0')
        if self.should_reject_by_topic(score, category_id):
            return True
        tweet_info = {
            'text': retweet_data['text'],
            'date': retweet_data['created_at'],
            'tweet_data': retweet_data,
            'category': category,
            'category_score': score,
            'model_data': pydash.get(annotated_data, 'labels'),
        }
        tweet_info = {**tweet_info, **retweet_data}
        print(tweet_info['category'], tweet_info['text'])
        print('https://twitter.com/i/web/status/' + tweet_info['id_str'])
        print()
        try:
            tweet_model = Tweet.from_dict(tweet_info)
            res = tweet_model.save(force_insert=True)
            print('rows effected: ', res)
        except Exception as e:
            print(e)
            print('rolling back')
            tweet_model.rollback()
        return True

    def on_error(self, status):
        print('error:', status)


def authorize():
    creds = json.load(open('credentials.json'))
    auth = OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
    auth.set_access_token(creds['access_token'], creds['access_token_secret'])
    return auth

def init_stream():
    listener = StdOutListener()
    auth = authorize()
    stream = Stream(auth, listener)
    stream.filter(track=['Trump', 'Mueller'],
                  filter_level='low',
                  async=True)

if __name__ == '__main__':
    init_stream()
