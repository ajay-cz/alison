# -*- coding: utf-8 -*-
from itertools import chain

import re
from flask import Flask, render_template, request

from pymongo import MongoClient

# configuration
MONGODB_HOST = '205.147.96.143'
MONGODB_PORT = 10065
MONGODB_NAME = 'kate'

# Flask app
app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

# DB Defaults
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = connection[MONGODB_NAME]
collection_name = 'bbc'

INIT_PAGE = 0
PAGE_LIMIT = 25

truthy = frozenset(('t', 'true', 'y', 'yes', 'on', '1'))

def asbool(s):
    """ Return the boolean value ``True`` if the case-lowered value of string
    input ``s`` is any of ``t``, ``true``, ``y``, ``on``, or ``1``, otherwise
    return the boolean value ``False``.  If ``s`` is the value ``None``,
    return ``False``.  If ``s`` is already one of the boolean values ``True``
    or ``False``, return it."""
    if s is None:
        return False
    if isinstance(s, bool):
        return s
    s = str(s).strip()
    return s.lower() in truthy

@app.route('/')
def home_page():
    """

    :return:
    """

    return render_template('home.html')


@app.route('/search')
def data_list():
    """

    :return:
    """
    page_number = int(request.args.get('page', INIT_PAGE))
    requested_page_count = int(request.args.get('item_count', PAGE_LIMIT))

    skip_page = (int(page_number) - 1) * requested_page_count if page_number > 0 else 0

    _query = {}
    params = request.args
    if params:
        for _filter in params.keys():
            _value = params.get(_filter, None)
            if _value:
                if _filter in ['media']:
                    if _value and _value in ['audio', 'video']:
                        _query.update({'media': _value.title()})
                if _filter in ['is_clip']:
                    if _value:
                        _query.update({'is_clip': asbool(_value)})
                if _filter in ['master_brand', 'service', 'title.Episode Title', 'title.Series Title']:
                    if _value:
                        _value = re.compile(re.escape(_value), re.IGNORECASE)
                        _query.update({_filter: {'$regex': _value, '$options': 'i'}})
                if _filter in ['categories', 'tags']:
                    if _value:
                        _query.update({_filter : {'$in': _value.split(',')}})
                if _filter in ['end_time']:
                    if _value:
                        _query.update({_filter: {'$lte': _value}})
                if _filter in ['start_time']:
                    if _value:
                        _query.update({_filter: {'$gte': _value}})

    print(_query)
    print(skip_page)
    print(requested_page_count)
    filtered_results = db[collection_name].find(_query).skip(int(skip_page)).limit(int(requested_page_count + 1)).sort([('start_time', -1)])

    # all_keys = {k for k in chain(*filtered_results)}
    # filtered_results.rewind()

    return render_template(
        'search.html',
        filtered_data=filtered_results,
        all_keys=[],
        result_count=filtered_results.count(),
        skip=skip_page,
        page_count=requested_page_count
    )
