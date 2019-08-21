#!/usr/bin/env python3

import argparse
import json
import os
import re
import sys
import termcolor


class JSON_Pattern:

    def __init__(self, json_string):
        self._result = False
        self.json = json.loads(json_string)


    def node_matches(self, subtree, _pattern=None):

        pattern = self.json['_pattern'] if _pattern is None else _pattern

        # DICTIONARIES
        if isinstance(subtree, dict):
            if not isinstance(pattern, dict):
                return False
            return set(pattern.keys()).intersection(set(subtree.keys())) == pattern.keys()

        # LISTS
        elif isinstance(subtree, list):
            return isinstance(pattern, list)

        # BASIC VALUES USING A MODIFIER PATTERN
        elif isinstance(pattern, dict) and len(pattern) is 1:
            # NEGATED VALUES
            if '_not' in pattern.keys():
                if isinstance(pattern['_not'], dict) and len(pattern['_not']) is 1:
                    return not self.node_matches(subtree, pattern['_not'])
                return not (subtree == pattern['_not'])
            # REGULAR EXPRESSIONS
            elif '_regex' in pattern.keys():
                return re.compile(pattern['_regex']).match(str(subtree))
        else:
            # SIMPLE VALUES
            return type(subtree) == type(pattern) and subtree == pattern


    def matches(self, tree, _pattern=None):

        pattern = self.json['_pattern'] if _pattern is None else _pattern

        if self.node_matches(tree, pattern):

            results = []

            if isinstance(tree, dict):
                for key, child_pattern in pattern.items():
                    results.append(self.matches(tree[key], _pattern=child_pattern))

            elif isinstance(tree, list):
                for child_pattern in pattern:
                    element_found=[]
                    for element in tree:
                        element_found.append(self.matches(element, _pattern=child_pattern))
                    results.append(any(element_found))

            else:
                results.append(True)

            if all(results):
                self._result = self._result or all(results)
            return all(results)

        else:

            results = []

            # DICTIONARIES
            if isinstance(tree, dict):
                for _, element in tree.items():
                    results.append(self.matches(element))

            # LISTS
            elif isinstance(tree, list):
                for element in tree:
                    results.append(self.matches(element))

            else:
                results.append(True)

            return any(results)

    def get_message(self):
        return self.json['_message']

    def evaluate(self, json_string):
        self.matches(json.loads(json_string))

        pattern_type = str(self.json.get('_type', 'info')).lower()

        if self._result:

            if pattern_type == 'info':
                termcolor.cprint(' - ' + self.get_message(), 'green')

            elif pattern_type in ['error', 'exception']:
                raise AssertionError(self.get_message())

        return self._result


def main():

    parser = argparse.ArgumentParser(description='Check JSON Document for patterns')
    parser.add_argument('pattern', type=str, nargs='+',
                        help="Files containing patterns to apply to the JSON-Document")

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-j', '--json', type=str, metavar='STR',
                        help='JSON to analyze as string. "-" for stdin')
    group.add_argument('-t', '--target', type=str, metavar='STR',
                        help='JSON-File to analyze.')

    args = parser.parse_args()

    # Read JSON to check
    if args.json is not None:
        json_string = sys.stdin if args.json is '-' else args.json
    elif args.target is not None:
        json_string = open(os.path.realpath(args.target), 'r').read()
    else:
        print('You need to specify a --target file or to pass --json data.')
        exit(1)

    termcolor.cprint('\nAnalysis of {0}\n'.format(os.path.realpath(args.target)), attrs=['bold'])

    # Read and create Patterns
    patterns = []
    for pattern_file in args.pattern:
        pattern_file = os.path.realpath(pattern_file)
        if os.path.isfile(pattern_file):
            patterns.append(JSON_Pattern(open(pattern_file, 'r').read()))

    # Check patterns
    error_found = False
    for pattern in patterns:
        try:
            pattern.evaluate(json_string)
        except AssertionError as e:
            termcolor.cprint(' - ' + str(e), 'red')
            error_found = True

    print()

    if error_found:
        exit(1)

if __name__ == '__main__':
    main()
