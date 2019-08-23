# Predicting the rating a reviewer will give a restaurant using Featuretools and the nlp-primitives library

<a style="margin:30px" href="https://www.featuretools.com">
    <img width=50% src="https://www.featuretools.com/wp-content/uploads/2017/12/FeatureLabs-Logo-Tangerine-800.png" alt="Featuretools" />
</a>

**When customers visit restaurants, they will oftentimes leave a review of some sort. Using data from TripAdvisor, we investigate how this text data can be used to predict the overall thoughts of the customer on that restuarant represented in a star rating.**

In this tutorial, we show how [Featuretools](https://www.featuretools.com) can be used alongside the [nlp-primitives](https://github.com/FeatureLabs/nlp_primitives) library to train an accurate machine learning model that can predict a customer's rating of a restaurant based on the text of their review and some information about the restaurant.

## Highlights

* We use the nlp-primitives library to create structured data from unstructured, hard to parse, text data
* We acheive an accuracy rating 40% higher than the baseline
* We use these primitives alongside Featuretools' `dfs` method to create as much information as possible from a dataset containing only two entities.
* The `dfs` method stacks the default primitives on top of the nlp-primitives to create new, data-rich, features.
* We build a pipeline that it can be reused for numerous NLP prediction problems (You can try this yourself!)

## Running the tutorial

1. Clone the repo

    ```
    git clone 
    ```

2. Install the requirements

    ```
    pip install -r requirements.txt
    ```
    
    
3. Download the data

    You can download the data directly from Kaggle [here](https://www.kaggle.com/jkgatt/restaurant-data-with-100-trip-advisor-reviews-each). Be sure to re-name it `reviews.json`, or change the file name in the tutorial.

4. Run the tutorial notebook, [Predict-Restaurant-Rating](predict-restaurant-rating.ipynb) using Jupyter

    ```
    jupyter notebook
    ```

## Feature Labs
<a href="https://www.featurelabs.com/">
    <img src="http://www.featurelabs.com/wp-content/uploads/2017/12/logo.png" alt="Featuretools" />
</a>

Featuretools is an open source project created by [Feature Labs](https://www.featurelabs.com/). To see the other open source projects we're working on visit Feature Labs [Open Source](https://www.featurelabs.com/open). If building impactful data science pipelines is important to you or your business, please [get in touch](https://www.featurelabs.com/contact).

### Contact

Any questions can be directed to help@featurelabs.com
