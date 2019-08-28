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

As soon as jMatch is installed, it is used to check `JSON/YAML` documents
against a predefined specification. jMatch uses `JSON/YAML` to define
specification options as a search pattern.

### Example Specification Pattern

**Example usecase:** Imagine, a bunch of JSON-formated config files, all of those
config files should specify the same text-encoding (*UTF-8*) to make sure that
all systems interoperate correctly.

**Solution:** To implement a solution for the given usecase, another
JSON-document needs to be specified, which contains at least the following data
concerning the given problem.

 - **type:** `info` or `error`
 - **message:** *A message to print if the pattern matches*
 - **pattern:** *An info or error case pattern that is searched in the document to check.


```javascript
[{
  "_type": "error",
  "_message": "The encoding should be UTF-8, but it is not.",
  "_pattern": {
    "encoding": {"_not": "UTF-8"}
  }
}]
```

We want to mark the problem as critical, we use the error type. If used in a
CI-pipeline, the type `error` forces the Pipeline to fail, if the pattern
matches. For the pattern we want to search for a encoding, with a value
different from *UTF-8*.

### Check if the pattern exists in a JSON document

If we want to check a `configfile.json` file if it matches our
`check-encoding-utf8.json`. We can perform the following operation, assuming
that both files are in our current working directory:

```sh
jmatch --target configfile.json check-encoding-utf8.json
```

If the configfile contains the pattern specified in `check-encoding-utf8.json`, the
`_message` specified is displayed.

### Check a file for multiple patterns

jMatch allows to check many patterns at once, therefore all pattern files must
be provided when running jMatch.

```sh
jmatch --target configfile.json pattern1.json pattern2.json [...]
```

To provide multiple pattern files for jMatch, wildcard expressions can be used,
to specify many pattern files easily:

```sh
jmatch --target hello.json pattern*.json
```

## Support

Please [open an issue](https://gitlab.rlp.net/jdillenberger/jmatch/issues/new) for support.
