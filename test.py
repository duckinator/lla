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

from pprint import pprint

from tokenizer import tokenize
from parser import parse




class Interpreter:
    def __init__(self, code, variables):
        self.tree = parse(tokenize(code))

    def run(self):
        print(self.tokens)



def main():
    programs = [
        "!website_up | !search & (!elasticsearch.http | !elasticsearch.process)",
        "!website_up & !search & ssh & search.local & elasticsearch.http & elasticsearch.process",
        "!website_up & !search & !ssh",
        "!website_up & !search & ssh & !elasticsearch.process",
        "!website_up & !search & ssh & !elasticsearch.http & elasticsearch.process",
        "website_up & !search",
    ]

    for program in programs:
        tokens = tokenize(program)
        parse_tree = parse(tokens)
        print(parse_tree)
        #Interpreter(tokens).run()


if __name__ == "__main__":
    main()
