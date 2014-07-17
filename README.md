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
		- payer: Antonio
		- date: 16/07/2014
		- amount: 20
		- people:
			- Alex
			- Barbara

The BillClin output for this history file will be:

	Alex owes Barbara 5.00
	Charlie owes Alex 5.00


# Caveats

- Obviously, you need to ensure that that each person has a unique name in the same history file.
- Dates are not mandatory, but it's a good thing that you keep history neat. BillClin will raise a warning in case you just forgot.
	

## Motivation

The library was created because BillPin had a serious history/totals inconsistency bug and they ignored emails/tweets reporting the issue. Hence, we needed a reliable yet simple alternative that by design doesn't make inconsistencies possible.

## Possible improvements

- Share bills unevenly.
- Merge of multiple history files, with deduplication of bills.
- Helper script to append bills to the history file.