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

def euclidean_distance(test, rest, length):
	distance = 0
	for x in range(length):
		for y in range(len(test[x])-1):
			distance += pow((test[x][y] - rest[x][y]), 2)
	return math.sqrt(distance)

def find_neighbors(test, rest, k):
	distances = []
	for x in range(len(rest)):
		result = euclidean_distance(test, rest[x], len(test))
		distances.append((rest[x], result))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def main():
	# prepare data
	array = load_csv_file('iris', 4)

	# prepare 10-fold-cross validation
	validation = []
	for x in xrange(0,10):
		validation.append(cross_validation(array, x))
	
	# generate predictions
	k = 1
	for x in xrange(0,10):
		test = validation[x]
		rest = list(validation)
		rest.pop(x)
		neighbors = find_neighbors(test, rest, k)
		print("test: %s" % (validation[x]))
		print("neighbors: %s\n" % (neighbors))

main()