#!/usr/bin/env python
#-*- coding: utf-8 -*-

import collections
import decimal
import yaml
import sys

D = decimal.Decimal

TWOPLACES = D('0.01')

history = yaml.load(open(sys.argv[1]).read())

# Keys in this dict are in the form (person1, person2)
# person1 should always come alphabetically before person2
# A positive amount means person 2 owes something to person 1
# A negative amount means person 1 owes something to person 2.
graph = collections.defaultdict(D)

for details in history:
    payer = details['payer']
    per_person = D(D(details['amount']) / len(details['people']
            )).quantize(TWOPLACES)
    for person in details['people']:
        if payer < person:
            graph[(payer, person)] += per_person
        elif payer > person:
            graph[(person, payer)] -= per_person

for (p1, p2), value in graph.iteritems():
    if value > 0:
        creditor, debitor = p1, p2
    elif value < 0:
        value *= -1
        creditor, debitor = p2, p1
    print "{} owes {} {}".format(debitor, creditor, value)

print ""
