
import re

def _extract_parsedef(fmt):
    '''Retrieve parse definition from the format string *fmt*.
    '''

    parsedef = []

    for part1 in fmt.split('}'):
        for part2 in part1.split('{'):
            if part2 is not '':
                if ':' in part2:
                    part2 = part2.split(':')
                    parsedef.append({part2[0]: part2[1]})
                else:
                    reg = re.search('(\{'+part2+'\})', fmt)
                    if reg:
                        parsedef.append({part2: None})
                    else:
                        parsedef.append(part2)

    return parsedef


def _extract_values( parsedef, stri):
    return {}


def _convert(convdef, stri):
    return 0.0


def parse( fmt, stri):
    pass
