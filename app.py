import datetime
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from refresh import fresh_quote

# initialize app and connect to mongo
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/spiritual")

@app.route('/')
def index():
    # get the data object from mongo
    meditations = mongo.db.meditations.find_one()

    # calculate amount of days since last refresh
    time_since_last_refresh = datetime.datetime.now() - meditations['meta']['last_refresh']
    days_since_last_refresh = time_since_last_refresh.days

    # if the quotes are at least a day old, get fresh ones and update the data object
    if days_since_last_refresh >= 1:
        thich_quote, thich_stale = fresh_quote(meditations['thich_quotes'], meditations['thich_stale'])
        got_saying, got_stale = fresh_quote(meditations['got_sayings'], meditations['got_stale'])
        # new refresh time will be 12am of today's date
        new_refresh_time = meditations['meta']['last_refresh'] + datetime.timedelta(days=days_since_last_refresh)
        # repackage all the data and overwrite the data dict
        meditations = {
            'thich_quotes' : meditations['thich_quotes'],
            'got_sayings' : meditations['got_sayings'],
            'thich_quote' : thich_quote,
            'got_saying' : got_saying,
            'thich_stale' : thich_stale,
            'got_stale' : got_stale,
            'meta' : {
                'last_refresh' : new_refresh_time
            }
        }
        # overwrite the db collection with the new data dict
        mongo.db.meditations.replace_one({}, meditations)

    # render today's quotes in the browser
    return render_template('index.html',meditations=meditations)


if __name__ == "__main__":
    app.run(debug=True, port=7777)
