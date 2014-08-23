# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#


from functools import partial
from .converters import ConverterManager
from .iso import get_countries_data

COUNTRIES = frozenset(country.alpha2 for country in get_countries_data())


class CountryConverterManager(ConverterManager):
    """:class:`~babelfish.converters.ConverterManager` for country converters"""
    entry_point = 'babelfish.country_converters'
    internal_converters = ['name = babelfish.converters.countryname:CountryNameConverter']

country_converters = CountryConverterManager()


class CountryMeta(type):
    """The :class:`Country` metaclass

    Dynamically redirect :meth:`Country.frommycode` to :meth:`Country.fromcode` with the ``mycode`` `converter`

    """
    def __getattr__(self, name):
        if name.startswith('from'):
            return partial(self.fromcode, converter=name[4:])
        return getattr(self, name)


class Country(CountryMeta(str('CountryBase'), (object,), {})):
    """A country on Earth

    A country is represented by a 2-letter code from the ISO-3166 standard

    :param string country: 2-letter ISO-3166 country code

    """
    def __init__(self, country):
        if country not in COUNTRIES:
            raise ValueError('%r is not a valid country' % country)

        #: ISO-3166 2-letter country code
        self.alpha2 = country

    @classmethod
    def fromcode(cls, code, converter):
        """Create a :class:`Country` by its `code` using `converter` to
        :meth:`~babelfish.converters.CountryReverseConverter.reverse` it

        :param string code: the code to reverse
        :param string converter: name of the :class:`~babelfish.converters.CountryReverseConverter` to use
        :return: the corresponding :class:`Country` instance
        :rtype: :class:`Country`

        """
        return cls(country_converters[converter].reverse(code))

    def __getattr__(self, name):
        return country_converters[name].convert(self.alpha2)

    def __hash__(self):
        return hash(self.alpha2)

    def __eq__(self, other):
        if other is None:
            return False
        return self.alpha2 == other.alpha2

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '<Country [%s]>' % self

    def __str__(self):
        return self.alpha2
