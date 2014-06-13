#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014

# Author(s):

# Panu Lahtinen <panu.lahtinen@fmi.fi>
# Hróbjartur Thorsteinsson <hroi@vedur.is>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


'''Parser class
'''

import re
import datetime as dt

class Parser(object):
    '''Parser class
    '''

    def __init__(self, fmt):
        self.fmt = fmt

    def parse(self, stri):
        '''Parse keys and corresponding values from *stri* using format
        described in *fmt* string.
        '''
        return parse(self.fmt, stri)

    def compose(self, keyvals):
        '''Return string composed according to *fmt* string and filled
        with values with the corresponding keys in *keyvals* dictionary.
        '''
        return compose(self.fmt, keyvals)

    def globify(self, keyvals):
        '''Generate a  string useable with glob.glob()  from format string
        *fmt* and *keyvals* dictionary.
        '''
        return globify(self.fmt, keyvals)

def _extract_parsedef(fmt):
    '''Retrieve parse definition from the format string *fmt*.
    '''

    parsedef = []
    convdef = {}

    for part1 in fmt.split('}'):
        for part2 in part1.split('{'):
            if part2 is not '':
                if ':' in part2:
                    part2 = part2.split(':')
                    parsedef.append({part2[0]: part2[1]})
                    convdef[part2[0]] = part2[1]
                else:
                    reg = re.search('(\{'+part2+'\})', fmt)
                    if reg:
                        parsedef.append({part2: None})
                    else:
                        parsedef.append(part2)

    return parsedef, convdef


def _extract_values(parsedef, stri):
    """
    Given a parse definition *parsedef* match and extract key value
    pairs from input string *stri*.
    """
    if len(parsedef) == 0:
        return {}

    match = parsedef.pop(0)
    # we allow ourselves typechecking
    # in case of this hidden subroutine
    if isinstance(match, str):
        # match
        if stri.find(match) == 0:
            stri_next = stri[len(match):]
            return _extract_values( parsedef, stri_next )
        else:
            raise ValueError
    else:
        key = list(match)[0]
        fmt = match[key]
        if (fmt is None) or (fmt.isalpha()):
            next_match = parsedef[0]
            value = stri[0:stri.find(next_match)]
            stri_next = stri[len(value):]
            keyvals =  _extract_values( parsedef, stri_next )
            keyvals[key] = value
            return keyvals
        else:
            # find number of chars
            num = _get_number_from_fmt(fmt)
            value = stri[0:num]
            stri_next = stri[len(value):]
            keyvals =  _extract_values( parsedef, stri_next )
            keyvals[key] = value
            return keyvals

def _get_number_from_fmt(fmt):
    """
    Helper function for _extract_values, 
    figures out string length from format string.
    """
    if '%' in fmt:
        # its datetime
        return len(("{0:"+fmt+"}").format(dt.datetime.now()))
    else:
        # its something else
        fmt = fmt.lstrip('0')
        return int(re.search('[0-9]+', fmt).group(0))


def _convert(convdef, stri):
    '''Convert the string *stri* to the given conversion definition
    *convdef*.
    '''

    if '%' in convdef:
        result = dt.datetime.strptime(stri, convdef)
    elif 'd' in convdef:

        if '>' in convdef:
            stri = stri.lstrip(convdef[0])
        elif '<' in convdef:
            stri = stri.rstrip(convdef[0])
        elif '^' in convdef:
            stri = stri.strip(convdef[0])
        else:
            pass

        result = int(stri)
    else:
        result = stri
    return result

def _collect_keyvals_from_parsedef(parsedef):
    '''Collect dict keys and values from parsedef.
    '''

    keys, vals = [], []

    for itm in parsedef:
        if isinstance(itm, dict):
            keys.append(list(itm.keys())[0])
            vals.append(list(itm.values())[0])

    return keys, vals

def parse(fmt, stri):
    '''Parse keys and corresponding values from *stri* using format
    described in *fmt* string.
    '''

    parsedef, convdef  = _extract_parsedef(fmt)
    keyvals = _extract_values(parsedef, stri)    

    for key in convdef.keys():        
        keyvals[key] = _convert(convdef[key], keyvals[key])

    return keyvals

def compose(fmt, keyvals):
    '''Return string composed according to *fmt* string and filled
    with values with the corresponding keys in *keyvals* dictionary.
    '''

    return fmt.format(**keyvals)

def globify(fmt, keyvals):
    '''Generate a string useable with glob.glob() from format string
    *fmt* and *keyvals* dictionary.
    '''

    parsedef, _ = _extract_parsedef(fmt)
    all_keys, all_vals = _collect_keyvals_from_parsedef(parsedef)
    replace_str = ''
    for key, val in zip(all_keys, all_vals):
        if key not in list(keyvals.keys()):
            # replace depending on the format defined in all_vals[key]
            if val is None:
                replace_str = '*'
            elif '%' in val:
                # calculate the length of datetime
                val2 = '{:'+val+'}'
                num = len(val2.format(dt.datetime.now()))
                replace_str = num * '?'
            elif not re.search('[0-9]+', val):
                if 'd' in val:
                    val2 = val.replace('d', 's')
                    fmt = fmt.replace(key+':'+val, key+':'+val2)
                replace_str = '*'
            else:
                if 'd' in val:
                    val2 = val.lstrip('0').replace('d', 's')
                    fmt = fmt.replace(key+':'+val, key+':'+val2)
                num = _get_number_from_fmt(val)
                replace_str = num * '?'
            keyvals[key] = replace_str
        else:
            # Check partial datetime usage
            if isinstance(keyvals[key], list) or \
                    isinstance(keyvals[key], tuple):
                conv_chars = keyvals[key][1]
            else:
                continue

            val2 = list(val)
            prev = 0
            datet = keyvals[key][0] # assume datetime
            while True:
                idx = val.find('%', prev)
                # Stop if no finds
                if idx == -1:
                    break
                if val[idx+1] not in conv_chars:
                    tmp = '{:%'+val[idx+1]+'}'
                    # calculate how many '?' are needed
                    num = len(tmp.format(datet))
                    val2[idx:idx+num] = num*'?'
                prev = idx+1
            val2 = ''.join(val2)
            fmt = fmt.replace(key+':'+val, key+':'+val2)
            keyvals[key] = keyvals[key][0]

    result = compose(fmt, keyvals)

    return result

