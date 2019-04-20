import sqlite3
import datetime
import gen_data
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.externals.joblib import load, dump


def gen_training_data(num):
    # Generate good data
    # Try [No, Low, Medium, High]
    colour_dict = {'yellow': 0, 'white': 0, 'green': 0, 'maroon': 1, 'red': 1, 'orange': 1, 'olive': 1, 'purple': 1, 'fuchsia': 1, 'lime': 1, 'navy': 1, 'blue': 1, 'aqua': 1, 'teal': 1,
                   'black': 1, 'gray': 1, 'silver': 1}
    urine_rec = {}
    gen_data.gen_good_data(int(num*0.65), urine_rec)
    urine_train_list = []
    for i in range(len(urine_rec['ph'])):
        urine_train_list.append([urine_rec['gravity'][i], urine_rec['ph'][i], urine_rec['bilirubin'][i], urine_rec['urobilinogen'][i], urine_rec['protein'][i], urine_rec['glucose'][i],
                                 urine_rec['ketones'][i], urine_rec['hemoglobin'][i], urine_rec['myoglobin'][i], urine_rec['leukocyte_esterase'][i], urine_rec['nitrite'][i],
                                 colour_dict[urine_rec['colour'][i]]])
    urine_train_label = ['No'] * len(urine_rec['ph'])

    # Generate low priority
    urine_rec = {}
    gen_data.gen_bad_data(int(num*0.20), urine_rec, 'low')
    for i in range(len(urine_rec['ph'])):
        urine_train_list.append([urine_rec['gravity'][i], urine_rec['ph'][i], urine_rec['bilirubin'][i], urine_rec['urobilinogen'][i], urine_rec['protein'][i], urine_rec['glucose'][i],
                                 urine_rec['ketones'][i], urine_rec['hemoglobin'][i], urine_rec['myoglobin'][i], urine_rec['leukocyte_esterase'][i], urine_rec['nitrite'][i],
                                 colour_dict[urine_rec['colour'][i]]])
    urine_train_label += ['Low'] * len(urine_rec['ph'])

    # Generate medium priority
    urine_rec = {}
    gen_data.gen_bad_data(int(num * 0.10), urine_rec, 'medium')
    for i in range(len(urine_rec['ph'])):
        urine_train_list.append([urine_rec['gravity'][i], urine_rec['ph'][i], urine_rec['bilirubin'][i], urine_rec['urobilinogen'][i], urine_rec['protein'][i], urine_rec['glucose'][i],
                                 urine_rec['ketones'][i], urine_rec['hemoglobin'][i], urine_rec['myoglobin'][i], urine_rec['leukocyte_esterase'][i], urine_rec['nitrite'][i],
                                 colour_dict[urine_rec['colour'][i]]])
    urine_train_label += ['Medium'] * len(urine_rec['ph'])

    # Generate high priority
    urine_rec = {}
    gen_data.gen_bad_data(int(num * 0.05), urine_rec, 'medium')
    for i in range(len(urine_rec['ph'])):
        urine_train_list.append([urine_rec['gravity'][i], urine_rec['ph'][i], urine_rec['bilirubin'][i], urine_rec['urobilinogen'][i], urine_rec['protein'][i], urine_rec['glucose'][i],
                                 urine_rec['ketones'][i], urine_rec['hemoglobin'][i], urine_rec['myoglobin'][i], urine_rec['leukocyte_esterase'][i], urine_rec['nitrite'][i],
                                 colour_dict[urine_rec['colour'][i]]])
    urine_train_label += ['High'] * len(urine_rec['ph'])

    return urine_train_list, urine_train_label


def scale_data(train, test):
    sc = StandardScaler()
    train = sc.fit_transform(train)
    test = sc.transform(test)
    return train, test, sc


def get_accuracy(pred_label, actual_label):
    a = [1 if pred_label[i] == actual_label[i] else 0 for i in range(len(pred_label))]
    return sum(a)/len(a)


def save_to_file(rf):
    with open('rfc', 'wb') as f:
        dump(rf, f)


def load_file():
    with open('rfc', 'rb') as f:
        rf = load(f)
    return rf


'''
if __name__ == '__main__':
    train_list, train_label = gen_training_data(1000000)
    X_train, X_test, y_train, y_test = train_test_split(train_list, train_label, test_size=0.2, random_state=0)
    # X_train, X_test, scaler = scale_data(X_train, X_test)

    # # Grid search
    # rfc = RandomForestClassifier(n_jobs=-1, max_features='sqrt', n_estimators=50, oob_score=True)
    # param_grid = {
    #     'n_estimators': [200, 500, 800, 1000],
    #     'max_features': ['auto', 'sqrt', 'log2'],
    #     'oob_score': [True, False]
    # }
    # CV_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5)
    # CV_rfc.fit(train_list, train_label)
    # print(CV_rfc.best_params_)
    #
    # # Predict using CV
    # test_list, test_label = gen_training_data(100)
    # pred = CV_rfc.predict(test_list)
    # print(f'Test accuracy: {get_accuracy(pred, test_label)}')

    # Actual classifier
    estimators = 1000
    classifier = RandomForestClassifier(n_estimators=estimators, random_state=0)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    print(f'Train accuracy: {get_accuracy(y_pred, y_test)}')
    save_to_file(classifier)

    rfc = load_file()
    # More tests
    print(f'Estimators: {estimators}')
    for i in range(5):
        test_list, test_label = gen_training_data(500)
        pred = rfc.predict(test_list)
        print('#################################')
        print(f'Test num {i} accuracy: {get_accuracy(pred, test_label)}')
        print(metrics.confusion_matrix(test_label, pred, labels=['No', 'Low', 'Medium', 'High']))
'''




