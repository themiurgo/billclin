# BillClin

BillClin is a command-line BillPin clone for geeks that like their shared billing to be reliable.

The way it works is pretty simple: one input file (the history), one output (the total).

## Usage

1. Write and maintain a history file (specs below).
2. `python billpin.py HISTORYFILE`.
3. Read output to know the current credit/debt status.

## The history file

The history file is a YAML formatted file that contains details of the various transactions. It is designed to be easily readable, flexible, yet formal.

Example: Alex has spent 15 $, shared between himself, Barbara and Charlie, for a sushi dinner. Later Barbara shared a taxi with Alex and she paid 20$.

	- Sushi Dinner:
		- payer: Alex
		- date: 16/07/2014
		- amount: 15
		- people:
			- Alex
			- Barbara
			- Charlie
	- Taxi:
		- payer: Barbara
		- date: 16/07/2014
		- amount: 20
		- people:
			- Alex
			- Barbara

The BillClin output for this history file will be:

	Alex owes Barbara 5.00
	Charlie owes Alex 5.00

## Unevenly shared bills

You have the possibility to share bills unevenly, by specifying a weight for each person in the history file. The default weight for each person is `1`.

For example, at the next `Spanish tapas` dinner, Barbara is bringing her boyfriend Dan, and will offer him a dinner. Therefore, she would pay two quotes. Dan won't appear in the list of people, as he is not involved in the billing.

	- Spanish tapas:
		- payer: Alex
		- date: 24/07/2014
		- amount: 50
		- people:
			- Alex
			- Barbara: 2
			- Charlie
			
Alex and Charlie are implicited given a weight of `1`.

This mechanism can be used also to indicate the exact amount spent by everyone, for example we could write, equivantly:

	- Spanish tapas:
		- payer: Alex
		- date: 24/07/2014
		- amount: 50
		- people:
			- Alex: 12.50
			- Barbara: 25
			- Charlie: 12.50

Note that BillClin **doesn't neither check or require** that weights total and the amount are the same. Every weight will be treated as a relative weight, w.r.t. the weights indicated for the other people.


# Caveats

- Obviously, you need to ensure that that each person has a unique name in the same history file.
- Dates are not mandatory, but it's a good thing that you keep history neat. BillClin will raise a warning in case you just forgot.
	

## Motivation

The library was created because BillPin had a serious history/totals inconsistency bug and they ignored emails/tweets reporting the issue. Hence, we needed a reliable yet simple alternative that by design doesn't make inconsistencies possible.

## Possible improvements

- Share bills unevenly.
- Merge of multiple history files, with deduplication of bills.
- Helper script to append bills to the history file.
