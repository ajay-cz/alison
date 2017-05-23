# -*- coding: utf-8 -*-
from collections import defaultdict
import math
from itertools import chain

import re
from flask import Flask, render_template, request

from pymongo import MongoClient

dev = False
# configuration
if dev:
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    MONGODB_NAME = 'kate'
else:
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
    Home Page
    :return:
    """

    return render_template('home.html')


def __merge_filter_values(c):
    """

    :param c:
    :return:
    """
    results = defaultdict(set)
    for i in c:
        results['service'].add(i.get('service', ''))
        results['Series Title'].add(i.get('title', {}).get('Series Title', ''))
        results['Episode Title'].add(i.get('title', {}).get('Episode Title', ''))
        results['media'].add(i.get('media', ''))
        results['start_time'].add(i.get('start_time', ''))
        results['end_time'].add(i.get('end_time', ''))
        results['is_clip'].add(i.get('is_clip', False))
        results['master_brand'].add(i.get('master_brand', False))
        results['tags'].add(it for it in i.get('tags', []))
        results['categories'].add(it for it in i.get('categories', []))

    return results


@app.route('/search')
def search_list():
    """ Search Page

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
                        # _query.update({_filter: {'$in': _value.split(',')}})
                        _query.update({_filter: {'$elemMatch': {'$regex': _value, '$options': 'i'}}})
                if _filter in ['end_time']:
                    if _value:
                        _query.update({_filter: {'$lte': _value}})
                if _filter in ['start_time']:
                    if _value:
                        _query.update({_filter: {'$gte': _value}})

        if not params.get('is_clip'):
            _query.update({'is_clip': False})

    filtered_results = db[collection_name].find(_query).skip(int(skip_page)).limit(int(requested_page_count))
    # .sort([('start_time', -1)])

    total_count = filtered_results.count()
    _real_count = filtered_results.count(1)
    # count = len(filtered_results)

    # all_keys = {k for k in chain(*filtered_results)}
    merged_filers = __merge_filter_values(filtered_results)

    filtered_results.rewind()

    pagination_links = []
    link_template = '%s' % (request.path)

    return render_template(
        'search.html',
        filtered_data=filtered_results,
        all_keys=[],
        result_count=_real_count,
        total_count=total_count,
        skip=skip_page,
        page_count=requested_page_count,
        filter_values=merged_filers,
        total_pages=int(round((total_count / requested_page_count) + 0.5))
    )
