# lla

Interpreter for a basic logic language, inspired by two-element boolean algebra.

## Demo

Here's a quick demo, based on the example that prompted its creation:

    >>> from lla.interpreter import Interpreter
    >>> variables = {
    ...     'ssh': True,
    ...     'website_up': True,
    ...     'search_up': False,
    ...     'elasticsearch.http': False,
    ...     'elasticsearch.process': True,
    ... }
    >>> interpreter = Interpreter(variables)
    >>> interpreter.run('ssh & website_up')
    True
    >>> interpreter.run('ssh & website_up & search_up')
    False
    >>> interpreter.run('!search_up & !elasticsearch.http & elasticsearch.process')
    True
    >>> interpreter.run('undefined_variable')
    Traceback (most recent call last):
        ...
    lla.interpreter.UndefinedVariableException: Undefined variable: undefined_variable

By replacing the `variables` dict with a class implementing `__getitem__`,
it becomes incredibly flexible.

## Overview

Here's the gist of it:

1. All variables are booleans.
2. You can't define variables in the language itself, but it be provided a
   `dict` or any object implementing `__getitem__`.
3. Only fully-resolvable statements are supported.
   a. Anything else raises a Python exception.
4. You provide the interpreter a single statement and it gets simplified to a single boolean value, which is then returned.


## Dependencies

In theory, all you need is Python 3.6+.

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/duckinator/lla.

The code for lla is available under the [MIT License](http://opensource.org/licenses/MIT).
