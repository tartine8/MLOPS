from datasets import load_dataset
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from string import punctuation
import joblib
import random

def preprocess(arr):
    return list(map(lambda t: t.lower().translate(str.maketrans(dict.fromkeys(punctuation))), arr))


def build_model():
    #Load data
    data = load_dataset("imdb")

    #Shuffle data
    tmp = dict(zip(data['train'][:]['text'], data['train'][:]['label']))
    keys = list(tmp.keys())
    random.shuffle(keys)
    tmp = [(key, tmp[key]) for key in keys]

    #Split data
    X_train = [key for key, val in tmp]
    y_train = [val for key, val in tmp]
    X_test = data["test"][:]["text"]
    y_test = data["test"][:]["label"]

    #preprocess data
    X_train = preprocess(X_train)
    X_test = preprocess(X_test)

    #Train and test model
    vectorizer = CountVectorizer()
    nbclassifier = MultinomialNB()
    pipeline = make_pipeline(vectorizer, nbclassifier)
    pipeline.fit(X_train, y_train)
    print(pipeline.score(X_train, y_train))
    print(pipeline.score(X_test, y_test))

    #Save model and training data
    joblib.dump(pipeline, 'imdb_model.joblib')
    joblib.dump(X_train, 'xtrain.joblib')

build_model()