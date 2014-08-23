# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from . import LanguageEquivalenceConverter
from ..iso import get_languages_data


class Alpha3BConverter(LanguageEquivalenceConverter):
    CASE_SENSITIVE = True
    SYMBOLS = {}
    for iso_language in get_languages_data():
        if iso_language.alpha3b:
            SYMBOLS[iso_language.alpha3] = iso_language.alpha3b
