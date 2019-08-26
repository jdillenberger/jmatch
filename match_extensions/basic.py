import re


def not_handler(pattern_handler, data):

    data['result'] = False
    if data['scope'] is 'node' and not isinstance(data['element'], (dict, list)):
        data['result'] = not data['element'] == data['pattern']

    return data


def regex_handler(pattern_handler, data):
    data['result'] = False
    if data['scope'] is 'node' and not isinstance(data['element'], (dict, list)):
        data['result'] = re.compile(data['pattern']).match(str(data['element']))

    return data
