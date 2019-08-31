#!/usr/bin/env python3
try:
    import typing
    import argparse
    import json
    import os
    import requests
    import sys
    import termcolor
    import pattern
    import yaml
except ImportError as error:
    print("There are missing dependencies for jmatch: \"{0}\"".format(error))
    exit(1)


def main():
    '''
    # Main Function
    execute hook for setuptools install
    defined in setup.py
    '''

    # Parse commandline arguments and create helppage
    parser = argparse.ArgumentParser(
            description='Simple test-suite for json/yaml files, optimized for CI pipelines.')

    parser.add_argument('pattern', type=str, nargs='+',
                        help="Files containing patterns to apply to the JSON-Document")

    group = parser.add_mutually_exclusive_group()

    group.add_argument('--stdin', action='store_true',
                       help='read document to check from `stdin`')
    group.add_argument('-f', '--file', type=str, metavar='STR',
                       help='read document to check from file.')
    group.add_argument('-u', '--url', type=str, metavar='STR',
                       help='read document to check from URL')

    parser.add_argument('--encoding', type=str, metavar='STR', default='UTF-8',
                        help='set file encoding - default is UTF-8')

    parser.add_argument('--prefix', type=str, metavar='STR', default='_',
                        help='meta and function prefix used by jMatch, default is "_"')

    parser.add_argument('--format', choices=['JSON', 'YAML'], default='json',
                        help='format of the document to check')

    parser.add_argument('-t', '--trace', action='store_true',
                        help='show routes to matching elements in the document')

    parser.add_argument('-p', '--path', action='store_true',
                        help='print the source path of the used pattern')

    parser.add_argument('-s', '--stats', action='store_true',
                        help='show statistics for all the performed checks')

    args = parser.parse_args()


    # Get data to check as string
    data: str = ''

    if args.stdin is True:
        data = str(sys.stdin.read())
    elif args.file is not None:
        path: str = os.path.realpath(args.file)
        if not os.path.exists(path):
            print('The file "{0}" does not exist.'.format(args.file))
        data = open(path, 'r', encoding=args.encoding).read()
    elif args.url is not None:
        request = requests.get(args.url)
        if request.status_code != 200:
            message = 'The url: "{0}" is not accessible. The request returned status code {1}'
            print(message.format(args.url, request.status_code))
            exit(1)
        data = request.text
    else:
        print('You need to specify a --target file, a --url or --stdin to read data.')
        exit(1)

    # Output Headline
    if args.file is not None:
        termcolor.cprint('\nAnalysis of {0}\n'.format(os.path.realpath(args.file)), attrs=['bold'])

    # Get pattern decoder
    decoder: typing.Union[typing.Callable, None] = None
    decode_format = str(args.format).lower()
    if decode_format in ['json']:
        decoder = json.loads
    elif decode_format in ['yml', 'yaml']:
        decoder = yaml.safe_load
    else:
        print('The specified format "{0}" is not supported.'.format(args.format))
        exit(1)

    # Create List of all patterns to check and their metadata
    checks: list = []
    required_names = ['message', 'type', 'pattern']
    for pattern_file in args.pattern:
        path = os.path.realpath(pattern_file)
        if not os.path.exists(path):
            print('The pattern file "{0}" does not exist.'.format(pattern_file))
            exit(1)
        try:
            decoded_check = decoder(open(path, 'r', encoding=args.encoding).read())
        except json.decoder.JSONDecodeError as e:
            print('The patternfile "{0}" is no valid JSON file.')

        required_keys = map(lambda s: '{0}{1}'.format(args.prefix, s.lower()), required_names)
        meta_wrong_error = 'Your Metadata is missing one of the folowing keys: {0} '

        def meta_ok(check: dict):
            return all(list(map(lambda x: x in check.keys(), required_keys)))

        if isinstance(decoded_check, list):
            for check in decoded_check:
                if not meta_ok(check):
                    exit(1)
                check['path'] = path
                checks.append(check)
        elif isinstance(decoded_check, dict):
            if not meta_ok(decoded_check):
                print(meta_wrong_error.format(required_keys))
                exit(1)
            checks.append(dict(**decoded_check, **{'path': pattern_file}))

    # Check all patterns and collect data
    exit_code: int = 0
    for idx, check in enumerate(checks):
        current_pattern = pattern.Pattern(check['{0}pattern'.format(args.prefix)], args.prefix)
        checks[idx]['matches'], checks[idx]['info'] = current_pattern.matches(decoder(data))
        if checks[idx]['matches'] and check['{0}type'.format(args.prefix)].lower() in ['error']:
            exit_code = 1

    # Display response
    for check in checks:
        if check['matches']:
            color = 'red' if check['{0}type'.format(args.prefix)] in 'error' else 'green'
            message = termcolor.colored(check['{0}message'.format(args.prefix)], color, attrs=['bold'])
            print(' ' * 2 + message + '\n')

            if args.path:
                message = ' ' * 4 + 'Pattern-file: \n      => "{0}"\n'
                print(termcolor.colored(message.format(check['path'])))

            if args.trace:
                print(termcolor.colored(' ' * 4 + 'Routes:'))
                for trace in check['info']['traces']:
                    print(' ' * 6 + '=> ' + (trace if trace != '' else "[]"))
                print()

    if args.stats:

        error_filter = lambda x: x['matches'] and x['{0}type'.format(args.prefix)] == 'error'
        summary = '{0} checks performed, {1} patterns matched, {2} of them are errors\n'.format(
            len(checks),
            len(list(filter(lambda x: x['matches'], checks))),
            len(list(filter(error_filter, checks)))
        )
        print('  {0} {1}'.format(termcolor.colored('Summary:', attrs=['bold']), summary))
    else:
        print()

    exit(exit_code)

if __name__ == '__main__':
    main()
