### How to format test files

#### Preface
`test.py`, when run, takes `*.test` files and runs the tests described within. These tests check that the regular expressions are performing as expected in order to catch an issues before being pushed to production. Which regular expressions are run and how they are run is defined in the file `test-conf.json`.

While reading this document, inspect the file `example.test` to help you understand the format.

#### Test Format
A test file can contain zero or more tests, which are technically defined as matching the following regular expression:
```regex
(?:%%%|!!!) *(.*)\n((?:.|\n)*?)~~~
```

A test starts with either `%%%` or `!!!`, depending on what kind of test it is.
A `%%%` test is a normal test that will only pass if the regular expression generates groups that match the expected output.
A `!!!` is a test that will only pass if the regular expression passed to it fails to match any groups. This will fail if even a single group is matched, so if you have a regular expression that captures an input in an odd way, change the regular expression or add a `%%%` test that captures the invalid input.

After the test header, you may have zero or more spaces and the name of the test. It is highly recommended for the test name to be unique among all test cases you have so you can more easily determine which test failed. The name may not contain newlines.

After this, the test contains data fields delimited by `~` characters on their own line. The first data field is the input, and the rest are the expected outputs. The test ends with `~~~`, which signifies that no more groups are being specified. Any characters outside a test case proper are ignored. You may not have comments inside of a test case.

As previously mentioned, the first data field is the input. It may span multiple lines, and ends with a `~` character.

Each of the other data fields are outputs from the regular expression(s) specified in `test-conf.json`. Each regular expression that is processed yields a list of groups and is described in one data field. Within each of these data fields, each group is on its own line.

Note: if you need newlines in a group output, any `\n` substrings are replaced with actual newlines, and any `\\` substrings are replaced with literal backslashes.

If the number of groups or the content in each differ from the expected output, the test will fail.

