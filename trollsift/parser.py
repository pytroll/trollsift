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
    - l: Make all characters lowercase by executing the parameter's `.lower()` method.
    - R: Remove all separators from the parameter including '-', '_', ' ', and ':'.
    - t: Title case the string by executing the parameter's `.title()` method.
    - u: Make all characters uppercase by executing the parameter's `.upper()` method.
    - h: A combination of 'R' and 'l'.
    - H: A combination of 'R' and 'u'.

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
# format_spec ::=  [[fill]align][sign][#][0][width][,][.precision][type]
# https://docs.python.org/3.4/library/string.html#format-specification-mini-language
fmt_spec_regex = re.compile(
    r'(?P<align>(?P<fill>.)?[<>=^])?(?P<sign>[\+\-\s])?(?P<pound>#)?(?P<zero>0)?(?P<width>\d+)?'
    r'(?P<comma>,)?(?P<precision>.\d+)?(?P<type>[bcdeEfFgGnosxX%])')


class RegexFormatter(string.Formatter):
    """String formatter that converts a format string to a regular expression.
    
    >>> regex_formatter = RegexFormatter()
    >>> regex_str = regex_formatter.format('{field_one:5d}_{field_two}')

    Can also be used to extract values from a string given the format spec
    for that string:

    >>> regex_formatter.extract_values('{field_one:5d}_{field_two}', '12345_sometext')
    {'field_one': '12345', 'field_two': 'sometext'}

    """

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

    @staticmethod
    def format_spec_to_regex(field_name, format_spec):
        """Make an attempt at converting a format spec to a regular expression."""
        # NOTE: remove escaped backslashes so regex matches
        regex_match = fmt_spec_regex.match(format_spec.replace('\\', ''))
        if regex_match is None:
            raise ValueError("Invalid format specification: '{}'".format(format_spec))
        regex_dict = regex_match.groupdict()
        fill = regex_dict['fill']
        ftype = regex_dict['type']
        width = regex_dict['width']
        align = regex_dict['align']
        # NOTE: does not properly handle `=` alignment
        if fill is None:
            if width is not None and width[0] == '0':
                fill = '0'
            elif ftype in ['s', 'd']:
                fill = ' '

        char_type = spec_regexes[ftype]
        if ftype == 's' and align and align.endswith('='):
            raise ValueError("Invalid format specification: '{}'".format(format_spec))
        final_regex = char_type
        if ftype in allow_multiple and (not width or width == '0'):
            final_regex += r'*'
        elif width and width != '0':
            if not fill:
                # we know we have exactly this many characters
                final_regex += r'{{{}}}'.format(int(width))
            elif fill:
                # we don't know how many fill characters we have compared to
                # field characters so just match all characters and sort it out
                # later during type conversion.
                final_regex = r'.{{{}}}'.format(int(width))
            elif ftype in allow_multiple:
                final_regex += r'*'

        return r'(?P<{}>{})'.format(field_name, final_regex)

    def regex_field(self, field_name, value, format_spec):
        if value != self.UNPROVIDED_VALUE:
            return super(RegexFormatter, self).format_field(value, format_spec)

        # Replace format spec with glob patterns (*, ?, etc)
        if not format_spec:
            return r'(?P<{}>.*)'.format(field_name)
        if '%' in format_spec:
            return r'(?P<{}>{})'.format(field_name, self._regex_datetime(format_spec))
        return self.format_spec_to_regex(field_name, format_spec)

    def format_field(self, value, format_spec):
        if not isinstance(value, tuple) or value[1] != self.UNPROVIDED_VALUE:
            return super(RegexFormatter, self).format_field(value, format_spec)
        field_name, value = value
        return self.regex_field(field_name, value, format_spec)

    def extract_values(self, fmt, stri):
        regex = self.format(fmt)
        match = re.match(regex, stri)
        if match is None:
            raise ValueError("String does not match pattern.")
        return match.groupdict()


regex_formatter = RegexFormatter()


def _get_number_from_fmt(fmt):
    """
    Helper function for extract_values,
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
        regex_match = fmt_spec_regex.match(convdef)
        match_dict = regex_match.groupdict() if regex_match else {}
        align = match_dict.get('align')
        pad = match_dict.get('fill')
        if align:
            # align character is the last one
            align = align[-1]
        if align and align in '<>^' and not pad:
            pad = ' '

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


def get_convert_dict(fmt):
    """Retrieve parse definition from the format string `fmt`."""
    convdef = {}
    for literal_text, field_name, format_spec, conversion in formatter.parse(fmt):
        if field_name is None:
            continue
        # XXX: Do I need to include 'conversion'?
        convdef[field_name] = format_spec
    return convdef


def parse(fmt, stri):
    """Parse keys and corresponding values from *stri* using format described in *fmt* string."""
    convdef = get_convert_dict(fmt)
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


def _generate_data_for_format(fmt):
    """Generate a fake data dictionary to fill in the provided format string."""
    # finally try some data, create some random data for the fmt.
    data = {}
    # keep track of how many "free_size" (wildcard) parameters we have
    # if we get two in a row then we know the pattern is invalid, meaning
    # we'll never be able to match the second wildcard field
    free_size_start = False
    for literal_text, field_name, format_spec, conversion in formatter.parse(fmt):
        if literal_text:
            free_size_start = False

        if not field_name:
            free_size_start = False
            continue

        # encapsulating free size keys,
        # e.g. {:s}{:s} or {:s}{:4s}{:d}
        if not format_spec or format_spec == "s" or format_spec == "d":
            if free_size_start:
                return None
            else:
                free_size_start = True

        # make some data for this key and format
        if format_spec and '%' in format_spec:
            # some datetime
            t = dt.datetime.now()
            # run once through format to limit precision
            t = parse(
                "{t:" + format_spec + "}", compose("{t:" + format_spec + "}", {'t': t}))['t']
            data[field_name] = t
        elif format_spec and 'd' in format_spec:
            # random number (with n sign. figures)
            if not format_spec.isalpha():
                n = _get_number_from_fmt(format_spec)
            else:
                # clearly bad
                return None
            data[field_name] = random.randint(0, 99999999999999999) % (10 ** n)
        else:
            # string type
            if format_spec is None:
                n = 4
            elif format_spec.isalnum():
                n = _get_number_from_fmt(format_spec)
            else:
                n = 4
            randstri = ''
            for x in range(n):
                randstri += random.choice(string.ascii_letters)
            data[field_name] = randstri
    return data


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
    data = _generate_data_for_format(fmt)
    if data is None:
        return False

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
