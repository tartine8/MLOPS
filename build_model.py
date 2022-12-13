from datasets import load_dataset
from string import punctuation
import fasttext
import random

def preprocess(arr):
    return list(map(lambda t: t.lower().translate(str.maketrans(dict.fromkeys(punctuation))), arr))

def fasttext_file(filename, x, y):
    file = open(filename, 'w')
    for i in range(len(x)):
        file.write(f"__label__{'positive' if y[i] == 1 else 'negative'} {x[i]}\n")
    file.close()

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

    #Convert data to fasttext files
    fasttext_file('train.txt', X_train, y_train)
    fasttext_file('test.txt', X_test, y_test)

    #Train and test model
    model = fasttext.train_supervised(input='train.txt')
    print('train values: ', model.test('train.txt'))
    print('test values: ', model.test('test.txt'))

    #Save model
    model.save_model('imdb_model.bin')

build_model()