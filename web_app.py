import flask
from sklearn.linear_model import LogisticRegression
import numpy as np
import ast

data_source = "/Users/ilya/Projects/geography_of_emotions/lonely_tweets.txt"

def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)

def last_tweet():
    with open(data_source, 'r') as d:
        data = d.readlines()
        text = remove_non_ascii(ast.literal_eval(data[-2])['text'])
    return text

# print last_line()

def get_n_last_tweets(n):
    with open(data_source, 'r') as d:
        data = d.readlines()
        n_tweets = []
        for nth_tweet in range(n):
            text = remove_non_ascii(ast.literal_eval(data[-(nth_tweet+2)])['text'])
            n_tweets.append(text)
    return n_tweets

# Initialize the app

app = flask.Flask(__name__)


# An example of routing:
# If they go to the page "/" (this means a GET request
# to the page http://127.0.0.1:5000/), return a simple
# page that says the site is up!


@app.route("/")
def hello():

    return str(last_tweet())


# Let's turn this into an API where you can post input data and get
# back output data after some calculations.

# If a user makes a POST request to http://127.0.0.1:5000/predict, and
# sends an X vector (to predict a class y_pred) with it as its data,
# we will use our trained LogisticRegression model to make a
# prediction and send back another JSON with the answer. You can use
# this to make interactive visualizations.

@app.route("/predict", methods=["POST"])
def predict():

    # read the data that came with the POST request as a dict
    data = flask.request.json

    # let's convert this into a numpy array so that we can
    # stick it into our model
    
    # x = np.array(data["example"]).reshape(-1,1)

    # # Classify!
    # y_pred = PREDICTOR.predict(x)

    # # Turn the result into a simple list so we can put it in
    # # a json (json won't understand numpy arrays)
    # y_pred = list(y_pred)

    # # Put the result in a nice dict so we can send it as json
    # results = {"predicted": y_pred}

    # Return a response with a json in it
    # flask has a quick function for that that takes a dict
    return flask.jsonify(get_n_last_tweets(data))


# Start the server, continuously listen to requests.
# We'll have a running web app!

# For local development:
app.run(debug=True)

# For public web serving:
# app.run(host='0.0.0.0')
