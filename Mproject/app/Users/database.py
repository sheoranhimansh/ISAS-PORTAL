import csv
import re

def creating_database():
	with open('a2.1.csv') as csvfile:
		readCSV = csv.reader(csvfile,delimiter = '\n')
		rows = []
		for row in readCSV:
			rows.append(row)
		print(rows)

creating_database()
