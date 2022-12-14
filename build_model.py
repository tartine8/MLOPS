from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
import joblib
import pandas as pd

def build_model():
    data = pd.read_csv('diabetes.csv')
    data = data.rename(columns={'Glucose': 'glucose', 'BMI': 'bmi', 'Age': 'age'})

    X = data[['glucose', 'bmi', 'age']]
    y = data['Outcome']

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model = LogisticRegression()
    model.fit(X_train, y_train)
    print('score:', model.score(X_test, y_test))

    joblib.dump(model, 'model.joblib')
    joblib.dump(X_test, 'xtest.joblib')
    joblib.dump(y_test, 'ytest.joblib')

build_model()