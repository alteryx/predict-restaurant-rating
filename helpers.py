import json
import nltk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import string
import sklearn
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

wn = nltk.WordNetLemmatizer()

def to_pd_arr(fp):
    tripreviews = open(fp).read()

    parsed_json = json.loads(tripreviews)
    holder_dict = {}
    counter = 0
    for rest in parsed_json['restaurants']:
        for review in rest['reviews']:
            holder_dict[counter] = {'title': review['review_title'], 'text': review['review_text'], 'date': review['review_date'], 'stars': review['review_rating'], 'price': rest['price']}
            counter += 1

    new_df = pd.DataFrame.from_dict(holder_dict, orient='index')

    return new_df

def clean_tokens(textstr):
    textstr = word_tokenize(textstr)
    processed = [ch.lower() for ch in textstr if ch not in
                                         set(string.punctuation).union(
                                         set(stopwords.words('english')))]
    processed = ['0' if re.search('[0-9]+', ch) else ch for ch in processed]
    processed = [wn.lemmatize(w) for w in processed]

    return processed


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    From: https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = sklearn.metrics.confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax