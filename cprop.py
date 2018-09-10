from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import NMF
import pandas as pd
import numpy as np
import re

def text_preprocessing(x):
    x = x.replace('http', ' http')
    x = strip_links(x)
    return x

def strip_links(x):
    stripped = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", x)
    return stripped

def load_data():
    df = pd.read_csv('data/top-tweets.csv')
    return df

def load_model():
    df = load_data()
    docs = df['text'].tolist()
    vectorizer = TfidfVectorizer(strip_accents = 'unicode',
                                 stop_words = 'english',
                                 lowercase = True,
                                 max_df = 0.5,
                                 min_df = 10)
    model = NMF(n_components=8,
                random_state=1,
                alpha=.1,
                l1_ratio=.5,
                init='nndsvd')
    model.fit(vectorizer.fit_transform(docs))
    print('model loaded')
    return model, vectorizer

def annotate_data(docs, model, vectorizer):
    cat_labels = {
        0: 'Trump/Russia/Putin',
        5: 'Mueller\'s Investigation',
        1: 'Billboards/Traveling/Spreading Awareness',
        7: 'Russian Money, International Influence',
        2: 'Speculation/Thanks',
        6: 'Statements of Fact',
        3: 'Alt-Right/Nazi/Bannon/GOP',
        4: 'Our president is a mobster',
    }
    data = model.transform(vectorizer.transform(docs))
    labels = {}
    top_cat = []
    top_cat_id = []
    scores = []
    for i, dp in enumerate(data):
        labels[i] = []
        for dpi, dpv in enumerate(dp):
            l = {'label': cat_labels[dpi], 'score': dpv, 'label_id': dpi}
            labels[i].append(l)
        topics = list(filter(lambda x: x['score'] > 0.01, labels[i]))
        labels[i] = topics
        sorted_topics = sorted(topics, key=lambda k: k['score'])
        score = sorted_topics[0]['score'] if len(sorted_topics) else 0
        top_topic = sorted_topics[0]['label'] if len(sorted_topics) else 'None'
        top_topic_id = sorted_topics[0]['label_id'] if len(sorted_topics) else 99
        top_cat.append(top_topic)
        top_cat_id.append(top_topic_id)
        scores.append(score)
    return {
        'labels': labels,
        'top_cat': top_cat,
        'top_cat_id': top_cat_id,
        'scores': scores,
    }

if __name__ == "__main__":
    import json
    import numpy as np
    model, vectorizer = load_model()
    input_data = [
        "trump putin russia",                 #0,
        "going don know say need really",     #1,
        "just reminder",                      #2,
        "white house nazi",                   #3,
        "president",                          #4,
        "mueller source investigation comey", #5,
        "like looks means",                   #6,
        "russian money laundering crime",     #7,
    ]
    results = annotate_data(input_data, model, vectorizer)
    expected = list(range(0, 8))
    assert expected == results['top_cat_id']
