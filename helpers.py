import featuretools as ft
import json
import pandas as pd
import warnings
import sys
import matplotlib.pyplot as plt
import sklearn
import numpy as np

from pandas.io.json import json_normalize

def file_to_es(basefile):
    with open(basefile) as f:
        d = json.load(f)

    restaurants = json_normalize(d['restaurants'])

    restaurants['id']=restaurants.index

    # the pair of name, address forms a unique key for each restaurant.
    unique_index = restaurants[['id','name','address']]

    restaurants = restaurants.drop(columns=['trip_advisor_url', 'name', 'country', 'locality', 'region', 'address', 'address_extended', 'reviews','tel', 'email', 'chain_name', 'fax', 'longitude', 'latitude', 'website','cuisine', 'hours.monday', 'hours.tuesday', 'hours.wednesday', 'hours.thursday', 'hours.friday', 'hours.saturday', 'hours.sunday'])

    reviews = json_normalize(d['restaurants'], record_path='reviews', meta=['name', 'address'])
    reviews['index']=reviews.index

    reviews = reviews.merge(unique_index, how='left', on=['name', 'address'])
    reviews = reviews.drop(columns=['name','address', 'review_url', 'review_website'])
    reviews = reviews.rename(columns={"id": "restaurant_id"})

    revs_types = {'review_title': ft.variable_types.Text,
                  'review_rating': ft.variable_types.Categorical}

    rest_types = {'rating': ft.variable_types.Categorical,
                  'name': ft.variable_types.Text}


    entities = {
        "restaurants" : (restaurants, "id"),
        "reviews" : (reviews, "index", None, revs_types)
    }

    relationships = [("restaurants", "id", "reviews", "restaurant_id")]


    es = ft.EntitySet("es", entities, relationships)

    es['reviews'].convert_variable_type('review_rating', ft.variable_types.Categorical)

    es.add_interesting_values()

    return es

def plot_confusion_matrix(y_true, y_pred, classes,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    From: https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
    """
    title = 'Normalized confusion matrix'

    # Compute confusion matrix
    cm = sklearn.metrics.confusion_matrix(y_true, y_pred)
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

    ax.set_ylim(len(cm)-0.5, -0.5)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], '.2f'),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    return ax