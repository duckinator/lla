#!/usr/bin/env python3

"""
1*1 = 1
1*0 = 0
1+1 = 1
1+0 = 1

character       ||  NEGATE_NEXT | IDENTIFIER | OPERATOR
================||=====================================
   !            ||    1         | 0          | 0
   &            ||    0         | 0          | 1
   |            ||    0         | 0          | 1
[a-zA-Z0-9.-]+
"""

from interpreter import Interpreter


def main():
    variables = {}
    interpreter = Interpreter(variables)

    variables['ssh'] = True
    variables['website_up'] = True
    variables['search'] = False
    variables['search.local'] = False
    variables['elasticsearch.http'] = False
    variables['elasticsearch.process'] = True

    assert interpreter.run(
        '(!search & (!elasticsearch.http | !elasticsearch.process)) | website_up'
    )
    assert interpreter.run(
        '!website_up | !search & (!elasticsearch.http | !elasticsearch.process)'
    )
    assert not interpreter.run(
        '!website_up & !search & ssh & search.local & elasticsearch.http & elasticsearch.process'
    )
    assert not interpreter.run(
        '!website_up & !search & !ssh'
    )
    assert not interpreter.run(
        '!website_up & !search & ssh & !elasticsearch.process'
    )
    assert not interpreter.run(
        '!website_up & !search & ssh & !elasticsearch.http & elasticsearch.process'
    )
    assert interpreter.run(
        'website_up    &    !search'
    )


if __name__ == "__main__":
    main()
