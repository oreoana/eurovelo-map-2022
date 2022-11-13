# `test`

For unit tests of source code.

`pytest` will automatically pick up any file that is named `test_`. There should
be one `test_` file per module in the `src` directory that can be tested. Within
each module test file, test classes should be prepended with `Test` and then the
name of the class under test. Test functions should have the form of `test__<classname>__<functionname>__<scenario>__<expected_result>`.
