"""
A simple REST API for returning emoji sentiment data based on research
from Institut "Jožef Stefan", Slovenia.
Research paper about how this data was compiled:
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0144296
Data for this API: http://kt.ijs.si/data/Emoji_sentiment_ranking/index.html
"""

import os
from functools import wraps

from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

MONGO_URL = os.environ.get('MONGO_URL')

CLIENT = MongoClient(MONGO_URL)

DB = CLIENT['emojinal']

KEYS = DB['keys']
EMOJI = DB['sentiment']

APP = Flask(__name__,static_folder='./landing', static_url_path='/')

APP.secret_key = os.environ.get('SECRET_KEY')

CORS(APP)

def auth_required(wrapped_function):
    """
    Decorator to check API key
    """
    @wraps(wrapped_function)
    def verify_key(*args, **kwargs):
        """
        Lookup key and redirect if presents
        """
        provided_key = request.headers.get('ApiKey')
        key = KEYS.find_one({'key': provided_key})
        if key:
            return wrapped_function(*args, **kwargs)
        return "Invalid key", 401
    return verify_key

@APP.route('/')
def index():
    """
    Serves a simple React page explaining the API
    """
    return APP.send_static_file('index.html')

@APP.route('/sentiment')
@APP.route('/sentiment/<emoji>')
@auth_required
def sentiment(emoji=None):
    """
    Return emoji sentiment scores and other metadata.
    Valid inputs include single Unicode codepoints
    and multiple emojis as strings. No input returns
    paginated emojis with option for query string size
    and page (default: ?size=5&page1)
    """
    if not emoji:
        page_size = int(request.args.get('size', 5))
        current_page = int(request.args.get('page', 1))
        skip_amount = page_size*(current_page-1)
        cursor = EMOJI.find({}, {'_id': 0}).skip(skip_amount).limit(page_size)
    else:
        codepoint = parse_codepoint_s(emoji)
        cursor = EMOJI.find({'unicodePoint': {"$in": codepoint}}, {'_id': 0})
    return jsonify(emojis=list(cursor))

def parse_codepoint_s(emoji):
    """
    Returns Unicode codepoint(s)
    """
    try:
        codepoint = [int(emoji)]
    except ValueError:
        try:
            codepoint = [ord(character) for character in emoji]
        except TypeError:
            codepoint = [0]
    finally:
        if not codepoint:
            codepoint = [0]
    return codepoint

if __name__ == '__main__':
    APP.run(host="0.0.0.0", debug=True)
