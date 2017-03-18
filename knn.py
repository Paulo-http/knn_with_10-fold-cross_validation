import csv
import random
import math
import operator

def load_csv_file(filename, attr):
	array = []
	with open(filename, 'rb') as csvfile:
	    lines = csv.reader(csvfile)
	    data = list(lines)
	    for x in range(len(data)):
	        for y in range(attr):
	            data[x][y] = float(data[x][y])
	        array.append(data[x])
	return array

def main():
	# prepare data
	array = load_csv_file('iris', 4)
	print array
	
main()	