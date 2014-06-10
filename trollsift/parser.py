import re
import datetime as dt

def _extract_parsedef( fmt ):
    return []


def _extract_values( parsedef, stri):
    """
    Given a parse definition, parsedef,  match and extract
    key value pairs from input string, stri.
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
        key = match.keys()[0]
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
            n = _get_number_from_fmt(fmt)
            value = stri[0:n]
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
        return len(("{:"+fmt+"}").format(dt.datetime.now()))
    else:
        # its something else
        return int(re.search('[0-9]+',fmt).group(0))


def _convert(convdef, stri):
    return 0.0


def parse( fmt, stri):
    pass
