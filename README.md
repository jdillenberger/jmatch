# jMatch

jMatch is a test-application for JSON files. It allows you to check JSON files
against a specification based on defined patterns. This is especially useful if
you need to check lots of JSON files for a given specification or if you want
to check your JSON files in a continuous integration pipeline.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Support](#support)

## Installation

### Install via PIP

Make sure, you have `python3` with `pip` installed. Use `pip` to install jMatch
in your shell as follows:

```sh
pip install jmatch
```

## Usage

After jMatch is installed, it is used to examine a JSON-File for patterns.
To check a file for patterns with jMatch, the following steps must be performed:

### Create pattern files

A pattern file is a JSON file that expects some special fields and provides
some semantic extensions.

A basic hello world example for a jMatch pattern would look like this:

```javascript
{
  "_type": "info",
  "_message": "The Document contains a 'hello world' value.",
  "_pattern": "Hello World"
}
```

This pattern would check whether the string "Hello World" exists as a value in
a given JSON document. More advanced example-patterns will be available in our wiki soon.

### Check if the pattern exists in a JSON document

If we want to check a `hello.json` file if it matches our `pattern1.json`. We
can perform the following operation, assuming that both files are in our
current working directory:

```sh
jmatch --target hello.json pattern1.json
```
If the `hello.json` file contains the pattern specified in `pattern1.json`, the
`_message` specified in `pattern1.json` is displayed.

### Check a file for multiple patterns

jMatch allows to check many patterns at once, therefore all pattern files must
be provided when running jMatch.

```sh
jmatch --target hello.json pattern1.json pattern2.json [...]
```

To provide multiple pattern files for jMatch, wildcard expressions can be used,
to specify many pattern files easily:

```sh
jmatch --target hello.json pattern*.json
```

## Support

Please [open an issue](https://gitlab.rlp.net/jdillenberger/jmatch/issues/new) for support.
