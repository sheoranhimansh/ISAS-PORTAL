import csv
import re
	
def creating_database_two():
	with open('a1.1.csv') as csvfile:
		readCSV = csv.reader(csvfile,delimiter = '\n')
		rows = []
		for row in readCSV:
			rows.append(row)
		print(rows)

creating_database_two()