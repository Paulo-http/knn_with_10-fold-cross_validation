import csv
import random
import math
import operator

def load_csv_file(filename, attr):
	array = []
	with open(filename, 'rb') as csvfile:
	    lines = csv.reader(csvfile, delimiter=';')	    
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
		distance += pow((test[x] - rest[x]), 2)
	return math.sqrt(distance)

def find_neighbors(test, rest, k):
	distances = []
	for x in range(len(rest)):
		for y in range(len(rest[x])):
			result = euclidean_distance(test[x], rest[x][y], len(test[x])-1)
			distances.append((rest[x][y], result))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def matrix_confusion(test, neighbors, matrix):
	error = 0.0
	for x in range(len(neighbors)):
		for y in range(len(test)):
			actual = test[y][-1]
			predicted = neighbors[x][-1]
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

def calc_accuracy(matrix):
	hits = 0.0
	mistakes = 0.0
	for key in matrix:
		classes = key.split()
		classes.pop(1)
		if classes[0] == classes[1]:
			hits += matrix[key]
		else:
			mistakes += matrix[key]
	return hits/(hits+mistakes)

def main():
	# prepare config
	# config = [['iris', 4, 3], ['adult', 14, 2], ['wine', 13, 3], ['cancer', 9, 2], ['quality', 11, 11], ['abalone', 8, 29]]
	config = [['iris.csv', 4, 3]]

	# start main loop
	for idx in range(len(config)):
		# prepare data
		filename = config[idx][0]
		attrs = config[idx][1]
		types = config[idx][2]
		csv = load_csv_file(filename, attrs)		
		length = len(csv)

		# prepare 10-fold-cross validation
		k_fold = 10
		validation = []
		for div in xrange(0,k_fold):
			validation.append(cross_validation(csv, div))
		
		# calculating m
		m = types
		if types%2 == 0:
			m += 1

		# calculating k
		k1 = 1
		k2 = m+2
		k3 = (m*10)+1
		k4 = (length/2)
		if length%2 == 0:
			k4 += 1
		k = [k1, k2, k3, k4]

		# generate predictions and create matrix of confusion
		for knn in k:
			matrix = {}
			cross_error = 0
			sample_error = {}

			for part in xrange(0,k_fold):
				test = validation[part]
				rest = list(validation)
				rest.pop(part)
				neighbors = find_neighbors(test, rest, knn)			
				error = matrix_confusion(test, neighbors, matrix)
				key = str(filename) + " p" + str(part+1)
				sample_error[key] = error
				cross_error += error
		
			# show results
			print("\n%d-knn in %s data set with %d elements:\n" % (knn, filename, len(csv)))
			print("matrix confusion:\n%s\n" % (matrix))
			print("sample error:\n%s\n" % (sample_error))
			print("cross validation error:\n%s\n" % (cross_error/k_fold))

			if types > 2:
				accuracy = calc_accuracy(matrix)
				print("accuracy:\n%s\n" % (accuracy))

main()

