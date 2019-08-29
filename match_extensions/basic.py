import re
import copy

def not_node(pattern_handler, data):

    if not isinstance(data['element'], (dict, list)):
        return not data['element'] == data['pattern']


def regex_node(pattern_handler, data):

    if data['scope'] is 'node' and not isinstance(data['element'], (dict, list)):
        return re.compile(data['pattern']).match(str(data['element']))
