#!/usr/bin/env python3
# coding: utf-8

"""Train and test machine learning model to weight WF relations."""

import re
import os
import sys
import argparse

import numpy as np
import pandas as pd
from math import log2
from collections import defaultdict
from collections import Counter

from sklearn.feature_selection import mutual_info_classif

from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import ComplementNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Perceptron
from sklearn.calibration import CalibratedClassifierCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import make_scorer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score

sys.path.append(os.path.realpath('../../@shared-scripts/'))
from feature_vector import make_vector  # noqa: E402
from split_data import split_data  # noqa: E402


# parse input parameters
parser = argparse.ArgumentParser()
parser.add_argument('-a', action='store', dest='a', required=True,
                    help='path to the anotated data')
parser.add_argument('-rel', action='store', dest='r', required=False,
                    help='path to the whole data')
parser.add_argument('-fsmi', action='store', dest='fsmi', required=False,
                    help='path to the file for returning MI of features')
parser.add_argument('-fsce', action='store', dest='fsce', required=False,
                    help='path to the file for returning CE of features')
parser.add_argument('-ev', action='store', dest='ev', required=False,
                    help='path to save performance of the model')
parser.add_argument('-p', action='store', dest='p', required=False,
                    help='path to the data to predict weights')
parser.add_argument('-m', action='store', dest='m', required=False,
                    help='name of model to predict weights')
parser.add_argument('-w', action='store', dest='w', required=False,
                    help='path to save file with weigted relations')
parser.add_argument('-dev', action='store_true', dest='dev', required=False,
                    help='developer mode for training model on heldout data')
par = parser.parse_args()


# load whole unlabeled data with custom features
custom_features = defaultdict(lambda: defaultdict())
if par.r:
    print('INFO: Loading custom features from whole data.')
    pass


# load data and assign features
print('INFO: Loading annotated data.')
annot_data = list()
relations = list()
with open(par.a, mode='r', encoding='U8') as f:
    for line in f:
        lab, parent, child = line.rstrip('\n').split('\t')
        relations.append((parent, child))
        child = child.split('_')
        parent = parent.split('_')
        lab = True if lab == '+' else False
        features = make_vector(parent=parent[1], parent_pos=parent[2][0],
                               child=child[1], child_pos=child[2][0],
                               custom={'Pid': parent[0], 'Cid': child[0]})
        annot_data.append({**features, **{'result': lab}})

# split annotated data on train/validation/holdout
divided = split_data(relations, train=0.65, validation=0.15, holdout=0.2,
                     random_seed=24)
for item in annot_data:
    parent = item['Pid'] + '_' + item['parent'] + '_' + item['parentPos']
    child = item['Cid'] + '_' + item['child'] + '_' + item['childPos']
    item['data'] = divided[(parent, child)]


# feature analysis/selection
if par.fsmi or par.fsce:
    # basic preprocessing
    dfc = pd.DataFrame(annot_data)
    dfc = dfc.drop(columns=['child', 'parent', 'Pid', 'Cid'], axis=1)

    # calculating mutual information
    if par.fsmi:
        print('INFO: Calculating mutual information for each feature.')
        k = [i for i in dfc.columns if i.endswith(('Par', 'Chi'))]
        addition = ['childPos', 'parentPos']
        for feature in k + addition:
            keys = list(set(dfc[feature].values))
            dfc[feature] = [keys.index(item) for item in dfc[feature]]
        x_cols = dfc.columns.difference(['result', 'data'])
        mi = mutual_info_classif(X=dfc[x_cols],
                                 y=dfc['result'], discrete_features=True)

        # save results
        with open(par.fsmi, mode='a', encoding='U8') as f:
            f.write('INPUT_DATA:\tECelex\n')
            for ft, val in zip(dfc[x_cols], mi):
                f.write(ft + '\t' + str(val) + '\n')
            f.write('\n')

    # calculating conditional entropy
    if par.fsce:
        print('INFO: Calculating conditional entropy for each feature.')
        cond_entrop = list()
        for feature in list(dfc.columns):
            if feature in ('result', 'data'):
                continue
            px = {v: list(dfc['result']).count(v) / len(dfc['result'])
                  for v in set(dfc['result'])}
            f = [tuple(t) for t in dfc[[feature, 'result']].values]
            pxy = {v: f.count(v)/len(dfc[[feature, 'result']]) for v in set(f)}
            ce = 0
            for pair in f:
                ce += pxy[pair] * log2((pxy[pair]) / (px[pair[1]]))
            cond_entrop.append((feature, (-1)*ce))

        # save results
        with open(par.fsce, mode='a', encoding='U8') as f:
            f.write('INPUT_DATA:\tECelex\n')
            for item in cond_entrop:
                f.write(item[0] + '\t' + str(item[1]) + '\n')
            f.write('\n')


# # load data for prediction and assign features
# predict_data = list()
# if par.p:
#     print('INFO: Loading data for prediction.')
#     with open(par.p, mode='r', encoding='U8') as f:
#         for line in f:
#             parent, child = line.rstrip('\n').split('\t')
#             child = child.split('_')
#             parent = parent.split('_')
#             features = make_vector(parent=parent[1], parent_pos=parent[2][0],
#                                    child=child[1], child_pos=child[2][0])
#             add = {'result': np.nan, 'data': 'P'}
#             predict_data.append({**features, **add})


# preprocess data for machine learning
# df = pd.DataFrame(annot_data + predict_data)
df = pd.DataFrame(annot_data)
train_df = df[df['data'] == 'T']
print('INFO: Including features into data.')
include_features = ('stTwChi', 'stThChi', 'stFoChi', 'stFiChi', 'stTwPar',
                    'stThPar', 'stFoPar', 'stFiPar', 'enTwPar', 'enThPar',
                    'enFoPar', 'enFiPar', 'enTwChi', 'enThChi', 'enFoChi',
                    'enFiChi', 'childPos', 'parentPos', 'levDist', 'data',
                    'jar_winDist', 'jacDist', 'lcsseq', 'lengthDif', 'result')

for feat in df.columns:  # exclude unused features
    if feat not in include_features:
        df = df.drop(columns=feat, axis=1)

print('INFO: Creating feature vectors.')
to_dummy = list(df.select_dtypes(include='object').columns)
to_dummy.remove('data')
if 'result' in to_dummy:
    to_dummy.remove('result')

for feat in to_dummy:
    # replace unknown/infreq values to NaN
    d = dict(df[df['data'] == 'T'][feat].value_counts())
    d = {k: k if f > 3 else np.nan for k, f in d.items()}
    df[feat] = df[feat].map(d)
    # one-hot representation of categorical features
    dummy = pd.get_dummies(df[feat], dummy_na=True, prefix=feat, sparse=True)
    dummy = dummy.drop(columns=feat + '_nan', axis=1)
    df = pd.concat([df, dummy], axis=1)
    df = df.drop(columns=feat, axis=1)
    dummy = None


# split data to train, heldout, and test datasets
print('INFO: Spliting data into train/heldout/test datasets.')
x_train = np.array(df[df['data'] == 'T'].drop(columns=['data', 'result']))
y_train = np.array(df[df['data'] == 'T']['result'].astype('bool'))
x_valid = np.array(df[df['data'] == 'V'].drop(columns=['data', 'result']))
y_valid = np.array(df[df['data'] == 'V']['result'].astype('bool'))
x_hold = np.array(df[df['data'] == 'H'].drop(columns=['data', 'result']))
y_hold = np.array(df[df['data'] == 'H']['result'].astype('bool'))


# machine learning classification models
classif = [
    (
        'Gaussian Naive Bayes',
        GaussianNB()
    ),
    (
        'Bernoulli Naive Bayes',
        BernoulliNB()
    ),
    (
        'COmplement Naive Bayes',
        ComplementNB()
    ),
    (
        'Multinomial Naive Bayes',
        MultinomialNB()
    ),
    (
        'LOGistic Regression',
        LogisticRegression(solver='liblinear', multi_class='ovr',
                           penalty='l2', random_state=24)
    ),
    (
        'LOGistic Regression 2',
        LogisticRegression(solver='saga', multi_class='ovr', l1_ratio=0.3,
                           penalty='elasticnet', max_iter=1000,
                           random_state=24)
    ),
    (
        'LOGistic Regression 3',
        LogisticRegression(solver='saga', multi_class='ovr', l1_ratio=0.5,
                           penalty='elasticnet', max_iter=1000,
                           random_state=24)
    ),
    (
        'LOGistic Regression 4',
        LogisticRegression(solver='saga', multi_class='ovr', l1_ratio=0.8,
                           penalty='elasticnet', max_iter=1000,
                           random_state=24)
    ),
    (
        'Decision Tree',
        DecisionTreeClassifier(criterion='entropy', min_samples_split=5,
                               random_state=24)
    ),
    (
        'Decision Tree 2',
        DecisionTreeClassifier(criterion='entropy', max_depth=10,
                               random_state=24)
    ),
    (
        'Decision Tree 3',
        DecisionTreeClassifier(criterion='entropy', min_samples_split=20,
                               random_state=24)
    ),
    (
        'Decision Tree 4',
        DecisionTreeClassifier(criterion='entropy', min_samples_split=50,
                               random_state=24)
    ),
    (
        'Random Forrest',
        RandomForestClassifier(criterion='entropy', min_samples_split=5,
                               random_state=24)
    ),
    (
        'Random Forrest 2',
        RandomForestClassifier(criterion='entropy', max_depth=20,
                               random_state=24)
    ),
    (
        'Random Forrest 3',
        RandomForestClassifier(criterion='entropy', min_samples_split=20,
                               random_state=24)
    ),
    (
        'Random Forrest 4',
        RandomForestClassifier(criterion='entropy', min_samples_split=50,
                               random_state=24)
    ),
    (
        'ADdaBOost',
        AdaBoostClassifier(n_estimators=100, random_state=24)
    ),
    (
        'PERceptron',
        CalibratedClassifierCV(Perceptron(max_iter=50, tol=-np.infty,
                                          random_state=24),
                               cv=10, method='isotonic')
    ),
    (
        'PERceptron 2',
        CalibratedClassifierCV(Perceptron(max_iter=100, tol=-np.infty,
                                          random_state=24),
                               cv=10, method='isotonic')
    ),
    (
        'KNeighbors Classifier',
        KNeighborsClassifier(n_neighbors=5)
    ),
    (
        'KNeighbors Classifier 2',
        KNeighborsClassifier(n_neighbors=2)
    ),
    (
        'Multi-Layer Perceptron',
        MLPClassifier(random_state=24)
    )
]


# machine learning evaluation metrics
def save_evaluation(cros_val, model, right, name):
    """Save results of models."""
    with open(par.ev, mode='a', encoding='U8') as f:
        f.write('RESULTS: ' + name + '\n')
        # cross-validation
        if cros_val is not None and cros_val.any():
            f.write('c-v acc: ' + str(cros_val['test_accuracy']) +
                    ' ' + str(np.mean(cros_val['test_accuracy'])) + '\n')
            f.write('c-v pre: ' + str(cros_val['test_precision']) +
                    ' ' + str(np.mean(cros_val['test_precision'])) + '\n')
            f.write('c-v rec: ' + str(cros_val['test_recall']) +
                    ' ' + str(np.mean(cros_val['test_recall'])) + '\n')
            f.write('c-v f1m: ' + str(cros_val['test_f1']) +
                    ' ' + str(np.mean(cros_val['test_f1'])) + '\n')
        # standard output model
        if model is not None and right is not None and \
           model.any() and right.any():
            f.write('model CMX:\n')
            f.write(str(confusion_matrix(right, model)) + '\n')
            f.write('m. acc: ' + str(accuracy_score(right, model)) + '\n')
            f.write('m. pre: ' + str(precision_score(right, model,
                                                     average='macro')) + '\n')
            f.write('m. rec: ' + str(recall_score(right, model,
                                                  average='macro')) + '\n')
            f.write('m. f1m: ' + str(f1_score(right, model,
                                              average='macro')) + '\n')
        f.write('\n')


scoring = {'f1': make_scorer(f1_score, average='macro'),
           'precision': make_scorer(precision_score, average='macro'),
           'recall': make_scorer(recall_score, average='macro'),
           'accuracy': make_scorer(accuracy_score)}


# machine learning training and testing
models = dict()
for name, model in classif:
    name = ''.join(re.findall(r'[A-Z0-9]', name))
    # selected model manually
    if par.m and par.m != name:
        continue
    print('INFO: Training', name, 'model.')
    # developer vs. classic mode
    if par.dev:
        # train and test developing model
        model.fit(x_train, y_train)
        y_pred = model.predict(x_valid)
        save_evaluation(None, y_pred, y_valid, name + '-devel')
        y_pred = model.predict(x_hold)
        save_evaluation(None, y_pred, y_hold, name + '-test')
    else:
        # train and test final model
        model.fit(x_train, y_train)
        y_pred = model.predict(x_hold)
        models[name] = model
        # save evaluation
        if par.ev:
            save_evaluation(None, y_pred, y_hold, name)


# # machine learning predict
# if par.p and par.m and par.w and par.m in models:
#     x_train, x_hold, x_valid, y_train, y_hold, y_valid = [None]*6  # save mem.
#     annot_data, predict_data, relations, divided = [None]*4  # save mem.
#     print('INFO: Predicting data for prediction.')
#     df = df[df['data'] == 'P'].drop(columns=['data', 'result'])
#     with open(par.p, mode='r', encoding='U8') as f:
#         for x_predict in np.array_split(df, 20):
#             y_prob = models[par.m].predict_proba(x_predict)
#             with open(par.w, mode='a', encoding='U8') as g:
#                 for weight in y_prob:
#                     relation = next(f).rstrip('\n').split('\t')
#                     relation.append(str(weight[1]))
#                     g.write('\t'.join(relation) + '\n')


# read big file in line-chunks
def read_in_chunks(file_obj, chunk=100000):
    lines, i = list(), 0
    while True:
        line = next(f, False)
        if not line:
            if lines != list():
                yield lines
            break
        line = line.rstrip('\n').split('\t')
        lines.append((line[0], line[1]))
        i += 1
        if i == chunk:
            yield lines
            i = 0
            lines = list()


def preprocess_features(df):
    include_features = ('stTwChi', 'stThChi', 'stFoChi', 'stFiChi', 'stTwPar',
                        'stThPar', 'stFoPar', 'stFiPar', 'enTwPar', 'enThPar',
                        'enFoPar', 'enFiPar', 'enTwChi', 'enThChi', 'enFoChi',
                        'enFiChi', 'childPos', 'parentPos', 'levDist', 'data',
                        'jar_winDist', 'jacDist', 'lcsseq', 'lengthDif',
                        'result')
    for feat in df.columns:  # exclude unused features
        if feat not in include_features:
            df = df.drop(columns=feat, axis=1)

    to_dummy = list(df.select_dtypes(include='object').columns)
    to_dummy.remove('data')
    if 'result' in to_dummy:
        to_dummy.remove('result')

    df_train = df[df['data'] == 'T']
    for feat in to_dummy:
        # replace unknown/infreq values to NaN
        d = dict(df_train[feat].value_counts())
        d = {k: k if f > 3 else np.nan for k, f in d.items()}
        df[feat] = df[feat].map(d)
        # one-hot representation of categorical features
        dummy = pd.get_dummies(df[feat], dummy_na=True, prefix=feat,
                               sparse=True)
        dummy = dummy.drop(columns=feat + '_nan', axis=1)
        df = pd.concat([df, dummy], axis=1)
        df = df.drop(columns=feat, axis=1)
        dummy = None

    # df_train = None
    # df.to_sparse()
    return df


# machine learning predict
if par.p and par.m and par.w and par.m in models:
    x_train, x_hold, x_valid, y_train, y_hold, y_valid = [None]*6  # save mem.
    annot_data, predict_data, relations, divided = [None]*4  # save mem.
    # predict
    j = 0
    print('INFO: Predicting data for prediction.')
    with open(par.p, mode='r', encoding='U8') as f:
        for lines in read_in_chunks(f):
            # create feature vectors
            # print('vector')
            predict_data = list()
            for line in lines:
                parent, child = line
                child = child.split('_')
                parent = parent.split('_')
                features = make_vector(parent=parent[1], parent_pos=parent[2],
                                       child=child[1], child_pos=child[2])
                add = {'result': np.nan, 'data': 'P'}
                predict_data.append({**features, **add})
            predict_data = pd.DataFrame(predict_data)
            # preprocess feature vectors
            # print('preproces')
            df = preprocess_features(pd.concat([train_df, predict_data], sort=True))
            df = df[df['data'] == 'P'].drop(columns=['data', 'result'])
            # predict and save
            # print('predict')
            with open(par.w, mode='a', encoding='U8') as g:
                # for x_predict in np.array_split(df, 50):
                    # y_prob = model.predict_proba(x_predict)
                y_prob = models[par.m].predict_proba(np.array(df))
                for weight, line in zip(y_prob, lines):
                    line = list(line)
                    line.append(str(weight[1]))
                    g.write('\t'.join(line) + '\n')
            j += 1
            print('Chunk', j, 'done.')
