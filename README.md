# ???

Interpreter for a basic logic language, inspired by two-element boolean algebra.

## Demo

Here's a quick demo, based on the example that prompted its creation:

    >>> from eh.interpreter import Interpreter
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
    eh.interpreter.UndefinedVariableException: Undefined variable: undefined_variable

## Overview

Here's the gist of it:

1. All variables are booleans.
2. You can't define variables, just pass the interpreter predefined values.
   a. Or pass the `Interpreter` instance a `dict`, because those are mutable.
3. Only fully-resolvable statements are supported.
   a. Anything else raises a Python exception.
4. You provide the interpreter a single statement and it gets simplified to a single boolean value, which is then return.


## Dependencies

In theory, this is all you need is Python 3.6+.

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/duckinator/snektrace.

The code for snektrace is available under the [MIT License](http://opensource.org/licenses/MIT).
