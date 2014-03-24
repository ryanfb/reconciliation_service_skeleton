#!/usr/bin/env python

"""
An example reconciliation service API for Google Refine 2.0.

See http://code.google.com/p/google-refine/wiki/ReconciliationServiceApi.
"""

import csv
from fuzzywuzzy import fuzz
import re
import sys
import simplejson as json
from flask import Flask, request, jsonify
app = Flask(__name__)


# Matching threshold.
match_threshold = 70

# Basic service metadata. There are a number of other documented options
# but this is all we need for a simple service.
metadata = {
    "name": "Pleiades Name Reconciliation Service",
    "view": {"url": "http://pleiades.stoa.org/places/{{id}}/"},
    "defaultTypes": [{"id": "/places", "name" : "Place"}]
    }

# Read in person records from csv file.
reader = csv.DictReader(open('pleiades-names-latest.csv', 'rb'))
records = [r for r in reader]


def search(query):

    # Initialize matches.
    matches = []

    # Search person records for matches.
    for r in records:
        score = fuzz.token_set_ratio(query, r['nameTransliterated'].decode('UTF-8'))
        
        if score > match_threshold:
            matches.append({
                    "id": r['pid'],
                    "name": r['nameTransliterated'].decode('UTF-8'),
                    "score": score,
                    "match": query == r['nameTransliterated'].decode('UTF-8'),
                    "type": [{"id": "/places", "name": "Place"}]
                    })
    
    print >> sys.stderr, matches
    return matches


def jsonpify(obj):
    """
    Like jsonify but wraps result in a JSONP callback if a 'callback'
    query param is supplied.
    """
    try:
        callback = request.args['callback']
        response = app.make_response("%s(%s)" % (callback, json.dumps(obj)))
        response.mimetype = "text/javascript"
        return response
    except KeyError:
        return jsonify(obj)


@app.route("/reconcile", methods=['POST', 'GET'])

def reconcile():
    # If a single 'query' is provided do a straightforward search.
    query = request.form.get('query')
    if query:
        # If the 'query' param starts with a "{" then it is a JSON object
        # with the search string as the 'query' member. Otherwise,
        # the 'query' param is the search string itself.
        if query.startswith("{"):
            query = json.loads(query)['query']
        results = search(query)
        return jsonpify({"result": results})

    # If a 'queries' parameter is supplied then it is a dictionary
    # of (key, query) pairs representing a batch of queries. We
    # should return a dictionary of (key, results) pairs.
    queries = request.form.get('queries')
    if queries:
        queries = json.loads(queries)
        results = {}
        for (key, query) in queries.items():
            results[key] = {"result": search(query['query'])}
        return jsonpify(results)

    # If neither a 'query' nor 'queries' parameter is supplied then
    # we should return the service metadata.
    return jsonpify(metadata)

if __name__ == '__main__':
    #print search("Doe, John")
    app.run(debug=True)
