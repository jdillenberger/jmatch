#!/usr/bin/env python3

import argparse
import json
import os
import requests
import sys
import termcolor
import pattern


def main():

    parser = argparse.ArgumentParser(description='Check file for patterns')
    parser.add_argument('pattern', type=str, nargs='+',
                        help="Files containing patterns to apply to the JSON-Document")

    group = parser.add_mutually_exclusive_group()

    group.add_argument('--stdin', action='store_true',
                        help='Read from `stdin`')
    group.add_argument('-f', '--file', type=str, metavar='STR',
                        help='File to check.')
    group.add_argument('-u', '--url', type=str, metavar='STR',
                        help='Online resource to check.')

    parser.add_argument('--encoding', type=str, metavar='STR', default='UTF-8',
                        help='File encoding - default is UTF-8')

    parser.add_argument('--prefix', type=str, metavar='STR', default='_',
                        help='Prefix for pattern functions line "not", default is "_"')

    parser.add_argument('--format', choices=['JSON', 'YAML'], default='json',
                        help='Specify the format to analyze, default is JSON')

    parser.add_argument('-t', '--trace', action='store_true',
                        help='Show routes to matching elements')

    parser.add_argument('-p', '--path', action='store_true',
                        help='Show name of the used pattern')

    parser.add_argument('-s', '--stats', action='store_true',
                        help='Show test statistics')
    args = parser.parse_args()

    data = str()

    # Get data to check as string
    if args.stdin is True:
        data = sys.stdin
    elif args.file is not None:
        path = os.path.realpath(args.file)
        if not os.path.exists(path):
            print('The file "{0}" does not exist.'.format(args.file))
        data = open(path, 'r', encoding=args.encoding).read()
    elif args.url is not None:
        request = requests.get(args.url, auth=('user', 'pass'))
        if request.status_code is not 200:
            message = 'The url: "{0}" is not accessible. The request returned status code {1}'
            print(message.format(args.url, request.status_code))
            exit(1)
        data = request.text
    else:
        print('You need to specify a --target file or to pass --json data.')
        exit(1)

    # Output Headline
    termcolor.cprint('\nAnalysis of {0}\n'.format(os.path.realpath(args.file)), attrs=['bold'])

    # Get pattern decoder
    decoder = None
    decode_format = str(args.format).lower()
    if decode_format in ['json']:
        decoder = json.loads
    elif decode_format in ['yml', 'yaml']:
        # ToDo: Implement YML-loader
        # decoder = ...
        pass
    else:
        print('The specified format "{0}" is not supported.'.format(args.format))
        exit(1)

    # Create List of all patterns to check and their metadata
    checks = []
    for pattern_file in args.pattern:
        path = os.path.realpath(pattern_file)
        if not os.path.exists(path):
            print('The pattern file "{0}" does not exist.'.format(pattern_file))
            exit(1)

        decoded_check = decoder(open(path, 'r', encoding=args.encoding).read())

        def meta_ok(check):
            required_keys = map(lambda s: '{0}{1}'.format(args.prefix, s.lower()), ['message', 'type', 'pattern'])
            return all(list(map(lambda x: x in check.keys(), required_keys)))

        if isinstance(decoded_check, list):
            for check in decoded_check:
                if not meta_ok(check):
                    # ToDo: Implement a more meaningful error message here
                    print('Your Metadata is not correct')
                    exit(1)
                checks.append(check + {'path': path})
        elif isinstance(decoded_check, dict):
            if not meta_ok(decoded_check):
                # ToDo: Implement a more meaningful error message here
                print('Your Metadata is not correct')
                exit(1)
            checks.append(dict(**decoded_check, **{'path': pattern_file}))

    # Check all patterns and collect data
    exit_code=0
    for idx, check in enumerate(checks):
        current_pattern = pattern.Pattern(check['{0}pattern'.format(args.prefix)], args.prefix)
        checks[idx]['matches'], checks[idx]['info'] = current_pattern.matches(decoder(data))
        if checks[idx]['matches'] and check['_type'].lower() in ['error']:
            exit_code=1

    # Display response
    for check in checks:
        if check['matches']:
            color = 'red' if check['_type'] in 'error' else 'green'
            message = termcolor.colored(check['_message'], color, attrs=['bold'])
            print(' ' * 2 + message + '\n')

            if args.path:
                print(termcolor.colored(' ' * 4 + 'Pattern-file: \n      => "{0}"\n'.format(check['path'])))


            if args.trace:
                print(termcolor.colored(' ' * 4 + 'Routes:'))
                for trace in check['info']['traces']:
                    print(' ' * 6 + '=> ' + (trace if trace is not '' else "[]"))
                print()
    if args.stats:
        summary = '{0} checks performed, {1} patterns matched, {2} of them are errors\n'.format(
            len(checks),
            len(list(filter(lambda x: x['matches'], checks))),
            len(list(filter(lambda x: x['matches'] and x['_type'] == 'error', checks)))
        )
        print('  {0} {1}'.format(termcolor.colored('Summary:', attrs=['bold']), summary))
    else:
        print()

    exit(exit_code)

if __name__ == '__main__':
    main()
