#!/usr/bin/env python
#-*- coding: utf-8 -*-

import collections
import decimal
import yaml
import sys

D = decimal.Decimal

TWOPLACES = D('0.01')

class History(object):
    def __init__(self):
        # Keys in this dict are in the form (person1, person2)
        # person1 should always come alphabetically before person2
        # A positive amount means person 2 owes something to person 1
        # A negative amount means person 1 owes something to person 2.
        self.graph = collections.defaultdict(D)

    def add_transaction(self, transaction):
        payer = transaction['payer']
        per_person = D(D(transaction['amount']) / len(transaction['people']
                )).quantize(TWOPLACES)
        for person in transaction['people']:
            if payer < person:
                self.graph[(payer, person)] += per_person
            elif payer > person:
                self.graph[(person, payer)] -= per_person

    def load(self, history):
        self.history = history
        for transaction in history:
            self.add_transaction(transaction)

    def print_total(self):
        for (p1, p2), value in self.graph.iteritems():
            if value > 0:
                creditor, debitor = p1, p2
            elif value < 0:
                value *= -1
                creditor, debitor = p2, p1
            print "{} owes {} {}".format(debitor, creditor, value)
        print ""

if __name__ == "__main__":
    history_data = yaml.load(open(sys.argv[1]).read())
    history = History()
    history.load(history_data)
    history.print_total()

