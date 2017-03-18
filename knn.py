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

def cross_validation(data, times):
	array = []
	lenght = range(len(data)/10)
	for x in lenght:
		array.append(data[x+len(lenght)*times])
	return array

def main():
	# prepare data
	array = load_csv_file('iris', 4)

	# prepare 10-fold-cross validation
	validation = []
	for x in xrange(0,10):
		validation.append(cross_validation(array, x))
	print validation
	
main()	