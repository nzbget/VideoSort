#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from collections import namedtuple
from pkg_resources import resource_stream  # @UnresolvedImport

from .compat import PY3
if PY3:
    from sys import intern


IsoCountry = namedtuple('IsoCountry', ['name', 'alpha2'])
IsoLanguage = namedtuple('IsoLanguage', ['alpha3', 'alpha3b', 'alpha3t', 'alpha2', 'scope', 'type', 'name', 'comment'])
IsoScript = namedtuple('IsoScript', ['code', 'number', 'name', 'french_name', 'pva', 'date'])


def get_countries_data():
    """Load countries ISO 3166-1 data

    :return: A generator of ISO 3166-1 Countries.
    :rtype: generator
    """
    f = resource_stream('babelfish', 'data/iso-3166-1.txt')
    try:
        f.readline()
        for l in f:
            l = l.decode('utf-8').strip().split(';')
            if PY3:
                l = (intern(s) for s in l)
            iso_country = IsoCountry(*l)
            yield iso_country
    finally:
        f.close()


def get_languages_data():
    """Load languages ISO 639-3 data

    :return: A generator of ISO 639-3 Languages.
    :rtype: generator
    """
    f = resource_stream('babelfish', 'data/iso-639-3.tab')
    try:
        f.readline()
        for l in f:
            l = l.decode('utf-8').split('\t')
            if PY3:
                l = (intern(s) for s in l)
            iso_language = IsoLanguage(*l)
            yield iso_language
    finally:
        f.close()


def get_scripts_data():
    """Load scripts ISO 15924 data

    :return: A generator of ISO 15924 Scripts.
    :rtype: generator
    """
    f = resource_stream('babelfish', 'data/iso15924-utf8-20131012.txt')
    try:
        f.readline()
        for l in f:
            l = l.decode('utf-8').strip()
            if not l or l.startswith('#'):
                continue
            l = l.split(';')
            if PY3:
                l = (intern(s) for s in l)
            script = IsoScript._make(l)
            yield script
    finally:
        f.close()
