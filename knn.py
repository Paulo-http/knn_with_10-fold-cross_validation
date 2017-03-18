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

def matrix_confusion(test, neighbors, matrix):
	error = 0.0
	lenght = 0.0
	for x in range(len(neighbors)):
		lenght = len(neighbors[x])
		for y in range(len(neighbors[x])):			
			actual = test[y][-1]
			predicted = neighbors[x][y][-1]
			current = actual + " | " + predicted
			mark_class(current, matrix)
			error += mark_error(actual, predicted)
	return error

def mark_class(current, matrix):
	if current in matrix:
		matrix[current] += 1			
	else:
		matrix[current] = 1

def mark_error(actual, predicted):
	if actual == predicted:
		return 0
	else:
		return 1

def main():
	# prepare config
	# config = [['iris', 4, 3], ['adult', 14, 2], ['wine', 13, 3], ['cancer', 9, 2], ['quality', 11, 11], ['abalone', 8, 29]]
	config = [['iris', 4, 3]]

	for x in range(len(config)):
		# prepare data
		filename = config[x][0]
		attrs = config[x][1]
		types = config[x][2]
		csv = load_csv_file(filename, attrs)

		# prepare 10-fold-cross validation
		validation = []
		for x in xrange(0,10):
			validation.append(cross_validation(csv, x))
				
		# generate predictions and create matrix of confusion
		k = 1		
		error = {}
		matrix = {}
		for x in xrange(0,10):
			test = validation[x]
			rest = list(validation)
			rest.pop(x)
			neighbors = find_neighbors(test, rest, k)
			key = "error p_" + str(x+1)
			error[key] = matrix_confusion(test, neighbors, matrix)				
		print matrix
		print error

main()