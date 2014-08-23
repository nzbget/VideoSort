# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals

from .iso import get_scripts_data

SCRIPTS = frozenset(script.code for script in get_scripts_data())


class Script(object):
    """A human writing system

    A script is represented by a 4-letter code from the ISO-15924 standard

    :param string script: 4-letter ISO-15924 script code

    """
    def __init__(self, script):
        if script not in SCRIPTS:
            raise ValueError('%r is not a valid script' % script)

        #: ISO-15924 4-letter script code
        self.code = script

    @property
    def name(self):
        """English name of the script"""
        return SCRIPTS[self.code]

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        return self.code == other.code

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '<Script [%s]>' % self

    def __str__(self):
        return self.code
