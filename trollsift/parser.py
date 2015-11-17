#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014, 2015

# Author(s):

# Panu Lahtinen <panu.lahtinen@fmi.fi>
# Hróbjartur Thorsteinsson <thorsteinssonh@gmail.com>

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
import random
import string
import six


class Parser(object):

    '''Parser class
    '''

    def __init__(self, fmt):
        self.fmt = fmt

    def __str__(self):
        return self.fmt

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

    def globify(self, keyvals=None):
        '''Generate a  string useable with glob.glob()  from format string
        *fmt* and *keyvals* dictionary.
        '''
        return globify(self.fmt, keyvals)

    def validate(self, stri):
        """
        Validates that string *stri* is parsable and therefore complies with
        this string format definition.  Useful for filtering strings, or to 
        check if a string if compatible before passing it to the
        parser function.
        """
        return validate(self.fmt, stri)

    def is_one2one(self):
        """
        Runs a check to evaluate if this format string has a
        one to one correspondence.  I.e. that successive composing and
        parsing opperations will result in the original data.
        In other words, that input data maps to a string,
        which then maps back to the original data without any change
        or loss in information.

        Note: This test only applies to sensible usage of the format string.
        If string or numeric data is causes overflow, e.g. 
        if composing "abcd" into {3s}, one to one correspondence will always 
        be broken in such cases. This off course also applies to precision 
        losses when using  datetime data.
        """
        return is_one2one(self.fmt)


def _extract_parsedef(fmt):
    '''Retrieve parse definition from the format string *fmt*.
    '''

    parsedef = []
    convdef = {}

    for part1 in fmt.split('}'):
        part2 = part1.split('{', 1)
        if part2[0] is not '':
            parsedef.append(part2[0])
        if len(part2) > 1 and part2[1] is not '':
            if ':' in part2[1]:
                part2 = part2[1].split(':', 1)
                parsedef.append({part2[0]: part2[1]})
                convdef[part2[0]] = part2[1]
            else:
                reg = re.search('(\{' + part2[1] + '\})', fmt)
                if reg:
                    parsedef.append({part2[1]: None})
                else:
                    parsedef.append(part2[1])
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
    # in case of this subroutine
    if isinstance(match, (str, six.text_type)):
        # match
        if stri.find(match) == 0:
            stri_next = stri[len(match):]
            return _extract_values(parsedef, stri_next)
        else:
            raise ValueError
    else:
        key = list(match)[0]
        fmt = match[key]
        fmt_list = ["%f", "%a", "%A", "%b", "%B", "%z", "%Z",
                    "%p", "%c", "%x", "%X"]
        if fmt is None or fmt.isalpha() or any([x in fmt for x in fmt_list]):
            if len(parsedef) != 0:
                next_match = parsedef[0]
                # next match is string ...
                if isinstance(next_match, (str, six.text_type)):
                    try:
                        count = fmt.count(next_match)
                    except AttributeError:
                        count = 0
                    pos = -1
                    for dummy in range(count + 1):
                        pos = stri.find(next_match, pos + 1)
                    value = stri[0:pos]
                # next match is string key ...
                else:
                    # pick out segment until string match,
                    # and parse in reverse,
                    rev_parsedef = []
                    x = ''
                    for x in parsedef:
                        if isinstance(x, (str, six.text_type)):
                            break
                        rev_parsedef.insert(0, x)
                    rev_parsedef = rev_parsedef + [match]
                    if isinstance(x, (str, six.text_type)):
                        rev_stri = stri[:stri.find(x)][::-1]
                    else:
                        rev_stri = stri[::-1]
                    # parse reversely and pick out value
                    value = _extract_values(rev_parsedef, rev_stri)[key][::-1]
            else:
                value = stri
            stri_next = stri[len(value):]
            keyvals = _extract_values(parsedef, stri_next)
            keyvals[key] = value
            return keyvals
        else:
            # find number of chars
            num = _get_number_from_fmt(fmt)
            value = stri[0:num]
            stri_next = stri[len(value):]
            keyvals = _extract_values(parsedef, stri_next)
            keyvals[key] = value
            return keyvals


def _get_number_from_fmt(fmt):
    """
    Helper function for _extract_values, 
    figures out string length from format string.
    """
    if '%' in fmt:
        # its datetime
        return len(("{0:" + fmt + "}").format(dt.datetime.now()))
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
    elif 'd' in convdef or 's' in convdef:
        try:
            align = convdef[0]
            if align in [">", "<", "^"]:
                pad = " "
            else:
                align = convdef[1]
                if align in [">", "<", "^"]:
                    pad = convdef[0]
                else:
                    align = None
                    pad = None
        except IndexError:
            align = None
            pad = None
        if align == '>':
            stri = stri.lstrip(pad)
        elif align == '<':
            stri = stri.rstrip(pad)
        elif align == '^':
            stri = stri.strip(pad)

        if 'd' in convdef:
            result = int(stri)
        else:
            result = stri
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

    parsedef, convdef = _extract_parsedef(fmt)
    keyvals = _extract_values(parsedef, stri)
    for key in convdef.keys():
        keyvals[key] = _convert(convdef[key], keyvals[key])

    return keyvals


def compose(fmt, keyvals):
    '''Return string composed according to *fmt* string and filled
    with values with the corresponding keys in *keyvals* dictionary.
    '''

    return fmt.format(**keyvals)


DT_FMT = {
    "%a": "*",
    "%A": "*",
    "%w": "?",
    "%d": "??",
    "%b": "*",
    "%B": "*",
    "%m": "??",
    "%y": "??",
    "%Y": "????",
    "%H": "??",
    "%I": "??",
    "%p": "*",
    "%M": "??",
    "%S": "??",
    "%f": "*",
    "%z": "*",
    "%Z": "*",
    "%j": "???",
    "%U": "??",
    "%W": "??",
    "%c": "*",
    "%x": "*",
    "%X": "*",
    "%%": "?"
}


def globify(fmt, keyvals=None):
    '''Generate a string useable with glob.glob() from format string
    *fmt* and *keyvals* dictionary.
    '''

    if keyvals is None:
        keyvals = {}
    else:
        keyvals = keyvals.copy()
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
                replace_str = val
                for fmt_key, fmt_val in DT_FMT.items():
                    replace_str = replace_str.replace(fmt_key, fmt_val)
                fmt = fmt.replace(key + ':' + val, key)
            elif not re.search('[0-9]+', val):
                if 'd' in val:
                    val2 = val.replace('d', 's')
                    fmt = fmt.replace(key + ':' + val, key + ':' + val2)
                replace_str = '*'
            else:
                if 'd' in val:
                    val2 = val.lstrip('0').replace('d', 's')
                    fmt = fmt.replace(key + ':' + val, key + ':' + val2)
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
            datet = keyvals[key][0]  # assume datetime
            while True:
                idx = val.find('%', prev)
                # Stop if no finds
                if idx == -1:
                    break
                if val[idx + 1] not in conv_chars:
                    tmp = '{0:%' + val[idx + 1] + '}'
                    # calculate how many '?' are needed
                    num = len(tmp.format(datet))
                    val2[idx:idx + num] = num * '?'
                prev = idx + 1
            val2 = ''.join(val2)
            fmt = fmt.replace(key + ':' + val, key + ':' + val2)
            keyvals[key] = keyvals[key][0]

    result = compose(fmt, keyvals)

    return result


def validate(fmt, stri):
    """
    Validates that string *stri* is parsable and therefore complies with
    the format string, *fmt*.  Useful for filtering string, or to 
    check if string if compatible before passing the string to the
    parser function.
    """
    try:
        parse(fmt, stri)
        return True
    except ValueError:
        return False


def is_one2one(fmt):
    """
    Runs a check to evaluate if the format string has a
    one to one correspondence.  I.e. that successive composing and
    parsing opperations will result in the original data.
    In other words, that input data maps to a string,
    which then maps back to the original data without any change
    or loss in information.

    Note: This test only applies to sensible usage of the format string.
    If string or numeric data is causes overflow, e.g. 
    if composing "abcd" into {3s}, one to one correspondence will always 
    be broken in such cases. This off course also applies to precision 
    losses when using  datetime data.
    """
    # look for some bad patterns
    parsedef, _ = _extract_parsedef(fmt)
    free_size_start = False
    for x in parsedef:
        # encapsulatin free size keys,
        # e.g. {:s}{:s} or {:s}{:4s}{:d}
        if not isinstance(x, (str, six.text_type)):
            pattern = list(x.values())[0]
            if (pattern is None) or (pattern == "s") or (pattern == "d"):
                if free_size_start:
                    return False
                else:
                    free_size_start = True
        else:
            free_size_start = False

    # finally try some data, create some random data for the fmt.
    data = {}
    for x in parsedef:
        try:
            key = list(x.keys())[0]
            formt = x[key]
            # make some data for this key and format
            if formt and '%' in formt:
                # some datetime
                t = dt.datetime.now()
                # run once through format to limit precision
                t = parse(
                    "{t:" + formt + "}", compose("{t:" + formt + "}", {'t': t}))['t']
                data[key] = t
            elif formt and 'd' in formt:
                # random number (with n sign. figures)
                if not formt.isalpha():
                    n = _get_number_from_fmt(formt)
                else:
                    # clearly bad
                    return False
                data[key] = random.randint(0, 99999999999999999) % (10 ** n)
            else:
                # string type
                if formt is None:
                    n = 4
                elif formt.isalnum():
                    n = _get_number_from_fmt(formt)
                else:
                    n = 4
                randstri = ''
                for x in range(n):
                    randstri += random.choice(string.ascii_letters)
                data[key] = randstri

        except AttributeError:
            pass

    # run data forward once and back to data
    stri = compose(fmt, data)
    data2 = parse(fmt, stri)
    # check if data2 equal to original data
    if len(data) != len(data2):
        return False
    for key in data:
        if key not in data2:
            return False
        if data2[key] != data[key]:
            return False
    # all checks passed, so just return True
    return True
