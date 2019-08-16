import featuretools as ft
import json
import pandas as pd
import warnings
import sys

from pandas.io.json import json_normalize

basefile = './reviews.json'

def file_to_es():
    with open(basefile) as f:
        d = json.load(f)

    restaurants = json_normalize(d['restaurants'])

    restaurants['id']=restaurants.index

    # the pair of name, address forms a unique key for each restaurant.
    unique_index = restaurants[['id','name','address']]

    restaurants = restaurants.drop(columns=['trip_advisor_url', 'name', 'address', 'address_extended', 'reviews','tel', 'email', 'chain_name', 'fax', 'longitude', 'latitude', 'website','cuisine', 'hours.monday', 'hours.tuesday', 'hours.wednesday', 'hours.thursday', 'hours.friday', 'hours.saturday', 'hours.sunday'])

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

    es.to_csv('./restaurants_entity_set')
    print("entityset has been created and is located in 'restaurants_entity_set' folder")

    if len(sys.argv) > 1:
        if sys.argv[1] == 'visualization':
            df = es['reviews'].df
            df.to_pickle('./visualization_df')
            print("dataframe for visualization has been created and stored in 'visualization_df' folder")



file_to_es()

