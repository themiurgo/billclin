#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function

import collections
import decimal
import yaml
import sys

D = decimal.Decimal

TWOPLACES = D('0.01')

class History(object):
    warning_fields = set(['description', 'date'])
    error_fields = set(['payer', 'people'])

    def __init__(self):
        # Keys in this dict are in the form (person1, person2)
        # person1 should always come alphabetically before person2
        # A positive amount means person 2 owes something to person 1
        # A negative amount means person 1 owes something to person 2.
        self.graph = collections.defaultdict(D)

    def add_transaction(self, transaction):
        payer = transaction['payer']
        people = []
        total_weight = D(0)
        for person in transaction['people']:
            try:
                person, weight = person.items()[0]
            except AttributeError:
                weight = 1
            weight = D(weight)
            people.append((person, weight))
            total_weight += weight
        total_weight = D(total_weight)
        per_person = D(D(transaction['amount']) / total_weight)

        for person, weight in people:
            person_amount = (per_person * weight).quantize(TWOPLACES)
            if payer < person:
                self.graph[(payer, person)] += person_amount
            elif payer > person:
                self.graph[(person, payer)] -= person_amount

    def load(self, history):
        self.history = history
        for i, transaction in enumerate(history):
            fields = transaction.keys()
            warning = self.warning_fields.difference(fields)
            error = self.error_fields.difference(fields)
            if warning:
                print("WARNING: Field(s) '{}' in transaction #{} are missing."
                    .format(', '.join(warning), i), file=sys.stderr)
            if error:
                print("ERROR: Field(s) '{}' in transaction #{} are missing. Skipping."
                    .format(', '.join(error), i), file=sys.stderr)
                continue
            self.add_transaction(transaction)

    def print_total(self):
        for (p1, p2), value in self.graph.iteritems():
            if value > 0:
                creditor, debitor = p1, p2
            elif value < 0:
                value *= -1
                creditor, debitor = p2, p1
            print("{} owes {} {}".format(debitor, creditor, value))
        print("")

if __name__ == "__main__":
    history_data = yaml.load(open(sys.argv[1]).read())
    history = History()
    history.load(history_data)
    history.print_total()

