import os
import json
from flask import Flask, render_template, request, redirect, url_for, Response
from db import Tweet

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/services/tweets', methods=['GET'])
def get_tweets():
  page = int(request.args.get('page'))
  limit = int(request.args.get('limit'))
  tweets_models = Tweet.select().order_by(Tweet.date.desc()).paginate(page, limit)
  tweets = [Tweet.to_dict(a)['tweet_data'] for a in tweets_models]
  body = {
      'tweets': tweets,
  }
  return Response(json.dumps(body), mimetype='application/json')

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  print('http://0.0.0.0:' + str(port))
  app.run(host='0.0.0.0', port=port, debug=True)

