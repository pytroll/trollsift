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


"""Parser class
"""

import re
import datetime as dt
import random
import string
import six


class Parser(object):
    """Parser class
    """

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

    format = compose

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


class StringFormatter(string.Formatter):
    """Custom string formatter class for basic strings.

    This formatter adds a few special conversions for assisting with common
    trollsift situations like making a parameter lowercase or removing
    hyphens. The added conversions are listed below and can be used in a
    format string by prefixing them with an `!` like so:

    >>> fstr = "{!u}_{!l}"
    >>> formatter = StringFormatter()
    >>> formatter.format(fstr, "to_upper", "To_LowerCase")
    "TO_UPPER_to_lowercase"

    - c: Make capitalized version of string (first character upper case, all lowercase after that) by executing the
      parameter's `.capitalize()` method.
    - h: A combination of 'R' and 'l'.
    - H: A combination of 'R' and 'u'.
    - l: Make all characters lowercase by executing the parameter's `.lower()` method.
    - R: Remove all separators from the parameter including '-', '_', ' ', and ':'.
    - t: Title case the string by executing the parameter's `.title()` method.
    - u: Make all characters uppercase by executing the parameter's `.upper()` method.

    """
    CONV_FUNCS = {
        'c': 'capitalize',
        'h': 'lower',
        'H': 'upper',
        'l': 'lower',
        't': 'title',
        'u': 'upper'
    }

    def convert_field(self, value, conversion):
        """Apply conversions mentioned above."""
        func = self.CONV_FUNCS.get(conversion)
        if func is not None:
            value = getattr(value, func)()
        elif conversion not in ['R']:
            # default conversion ('r', 's')
            return super(StringFormatter, self).convert_field(value, conversion)

        if conversion in ['h', 'H', 'R']:
            value = value.replace('-', '').replace('_', '').replace(':', '').replace(' ', '')
        return value


formatter = StringFormatter()


def _extract_parsedef(fmt):
    """Retrieve parse definition from the format string `fmt`."""
    parsedef = []
    convdef = {}
    for literal_text, field_name, format_spec, conversion in formatter.parse(fmt):
        if literal_text:
            parsedef.append(literal_text)
        if field_name is None:
            continue
        parsedef.append({field_name: format_spec or None})
        convdef[field_name] = format_spec
    return parsedef, convdef


# taken from https://docs.python.org/3/library/re.html#simulating-scanf
spec_regexes = {
    'c': r'.',
    'd': r'[-+]?\d',
    'f': r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?',
    'i': r'[-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)',
    'o': r'[-+]?[0-7]',
    's': r'\S',
    'x': r'[-+]?(0[xX])?[\dA-Fa-f]',
}
spec_regexes['e'] = spec_regexes['f']
spec_regexes['E'] = spec_regexes['f']
spec_regexes['g'] = spec_regexes['f']
spec_regexes['X'] = spec_regexes['x']
allow_multiple = ['c', 'd', 'o', 's', 'x', 'X']


class RegexFormatter(string.Formatter):

    # special string to mark a parameter not being specified
    UNPROVIDED_VALUE = '<trollsift unprovided value>'
    ESCAPE_CHARACTERS = [x for x in string.punctuation if x not in '\\%']
    ESCAPE_SETS = [(c, '\{}'.format(c)) for c in ESCAPE_CHARACTERS]

    def _escape(self, s):
        """Escape bad characters for regular expressions.

        Similar to `re.escape` but allows '%' to pass through.

        """
        for ch, r_ch in self.ESCAPE_SETS:
            s = s.replace(ch, r_ch)
        return s

    def parse(self, format_string):
        parse_ret = super(RegexFormatter, self).parse(format_string)
        for literal_text, field_name, format_spec, conversion in parse_ret:
            # the parent class will call parse multiple times moving
            # 'format_spec' to 'literal_text'. We only escape 'literal_text'
            # so we don't escape things twice.
            literal_text = self._escape(literal_text)
            yield literal_text, field_name, format_spec, conversion

    def get_value(self, key, args, kwargs):
        try:
            return super(RegexFormatter, self).get_value(key, args, kwargs)
        except (IndexError, KeyError):
            return key, self.UNPROVIDED_VALUE

    def _regex_datetime(self, format_spec):
        replace_str = format_spec
        for fmt_key, fmt_val in DT_FMT.items():
            if fmt_key == '%%':
                # special case
                replace_str.replace('%%', '%')
                continue
            count = fmt_val.count('?')
            # either a series of numbers or letters/numbers
            regex = r'\d{{{:d}}}'.format(count) if count else r'[^ \t\n\r\f\v\-_:]+'
            replace_str = replace_str.replace(fmt_key, regex)
        return replace_str

    def regex_field(self, value, format_spec):
        if value != self.UNPROVIDED_VALUE:
            return super(RegexFormatter, self).format_field(value, format_spec)

        # Replace format spec with glob patterns (*, ?, etc)
        if not format_spec:
            return r'.*'
        if '%' in format_spec:
            return self._regex_datetime(format_spec)
        char_type = spec_regexes[format_spec[-1]]
        num_match = re.search('[0-9]+', format_spec)
        num = 0 if num_match is None else int(num_match.group(0))
        has_multiple = format_spec[-1] in allow_multiple
        if num == 0 and has_multiple:
            # don't know the count
            return r'{}*'.format(char_type)
        elif num == 0:
            # floats and other types can't have multiple
            return char_type
        elif format_spec[-1] in allow_multiple:
            return r'{}{{{:d}}}'.format(char_type, num)
        else:
            return r'{}'.format(char_type)

    def format_field(self, value, format_spec):
        if not isinstance(value, tuple) or value[1] != self.UNPROVIDED_VALUE:
            return super(RegexFormatter, self).format_field(value, format_spec)
        field_name, value = value
        new_value = self.regex_field(value, format_spec)
        return '(?P<{}>{})'.format(field_name, new_value)

    def extract_values(self, fmt, stri):
        regex = self.format(fmt)
        match = re.match(regex, stri)
        if match is None:
            raise ValueError("String does not match pattern.")
        return match.groupdict()


regex_formatter = RegexFormatter()


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
    """Convert the string *stri* to the given conversion definition *convdef*."""
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


def parse(fmt, stri):
    '''Parse keys and corresponding values from *stri* using format
    described in *fmt* string.
    '''

    parsedef, convdef = _extract_parsedef(fmt)
    keyvals = regex_formatter.extract_values(fmt, stri)
    for key in convdef.keys():
        keyvals[key] = _convert(convdef[key], keyvals[key])

    return keyvals


def compose(fmt, keyvals):
    """Convert parameters in `keyvals` to a string based on `fmt` string."""
    return formatter.format(fmt, **keyvals)


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


class GlobifyFormatter(string.Formatter):

    # special string to mark a parameter not being specified
    UNPROVIDED_VALUE = '<trollsift unprovided value>'

    def get_value(self, key, args, kwargs):
        try:
            return super(GlobifyFormatter, self).get_value(key, args, kwargs)
        except (IndexError, KeyError):
            # assumes that
            return self.UNPROVIDED_VALUE

    def format_field(self, value, format_spec):
        if not isinstance(value, (list, tuple)) and value != self.UNPROVIDED_VALUE:
            return super(GlobifyFormatter, self).format_field(value, format_spec)
        elif value != self.UNPROVIDED_VALUE:
            # partial provided date/time fields
            # specified with a tuple/list of 2 elements
            # (value, partial format string)
            value, dt_fmt = value
            for fmt_letter in dt_fmt:
                fmt = '%' + fmt_letter
                format_spec = format_spec.replace(fmt, value.strftime(fmt))

        # Replace format spec with glob patterns (*, ?, etc)
        if not format_spec:
            return '*'
        if '%' in format_spec:
            replace_str = format_spec
            for fmt_key, fmt_val in DT_FMT.items():
                replace_str = replace_str.replace(fmt_key, fmt_val)
            return replace_str
        if not re.search('[0-9]+', format_spec):
            # non-integer type
            return '*'
        return '?' * _get_number_from_fmt(format_spec)


globify_formatter = GlobifyFormatter()


def globify(fmt, keyvals=None):
    """Generate a string usable with glob.glob() from format string
    *fmt* and *keyvals* dictionary.
    """
    if keyvals is None:
        keyvals = {}
    return globify_formatter.format(fmt, **keyvals)


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
    be broken in such cases. This of course also applies to precision
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
