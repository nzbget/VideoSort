#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from array import array


class ArrayDataTable(object):
    """A full-memory strings data structure, loaded from a delimited text file."""
    def __init__(self, rows_iterable, encoding='utf-8', delimiter='\t', skip_columns=None):
        self.rows = 0
        self.columns = 0
        self.encoding = encoding
        self.delimiter = delimiter
        self.skip_columns = skip_columns
        self._data_array = array('b')
        self._pos_array = array('i')
        for row in rows_iterable:
            self._init_row(row)
            self.rows = self.rows + 1

    def _init_row(self, row):
        row_data = row.decode(self.encoding).split(self.delimiter)
        self.columns = 0
        i = 0
        for u in row_data:
            if not self.skip_columns or i not in self.skip_columns:
                b = len(self._data_array)
                self._data_array.fromstring(u.encode(self.encoding))
                self._pos_array.append(b)
                self.columns += 1
            i += 1

    def get(self, row, column):
        start = self._pos_array[row * self.columns + column]
        end = self._pos_array[row * self.columns + column + 1]

        value_array = array('b')
        for i in range(start, end):
            value_array.append(self._data_array[i])

        return value_array.tostring().decode(self.encoding)  # tostring() = tobytes() before 3.2

    def __len__(self):
        return self.rows


class MmapDataTable(object):
    """A mmap-based strings data structure, loaded from a delimited text file."""
    def __init__(self, mmap_object, encoding='utf-8', delimiter='\t', skip_columns=None):
        self._data_mmap = mmap_object
        self.encoding = encoding
        self.delimiter = delimiter
        self.rows = 0
        self.columns = 0
        self.skip_columns = skip_columns
        self._pos_array = array('i')
        self._offset = self._data_mmap.tell()
        for row in iter(self._data_mmap.readline, b''):
            self._init_row(row)
            self.rows = self.rows + 1
            self._offset = self._data_mmap.tell()

    def _init_row(self, row):
        row_data = row.decode(self.encoding).split(self.delimiter)
        self.columns = 0
        pos = self._offset
        i = 0
        for u in row_data:
            if not self.skip_columns or i not in self.skip_columns:
                self._pos_array.append(pos)
                self.columns += 1
            pos = pos + len(u.encode(self.encoding)) + len(self.delimiter)
            i += 1

    def get(self, row, column):
        start = self._pos_array[row * self.columns + column]
        end = self._pos_array[row * self.columns + column + 1]

        data = self._data_mmap[start:end - 1]
        decoded_data = data.decode(self.encoding)
        if not self.skip_columns:
            return decoded_data
        else:
            return decoded_data.split(self.delimiter)[0]

    def __len__(self):
        return self.rows
