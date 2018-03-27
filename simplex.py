#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import argparse
import numpy as np

from SimplexMethod import SimplexMethod

def open_file(file_name):
	try:
		file = open(file_name, "r")
		line = file.read()
		if line.find('min') != -1:
			print("es min")
			type = 1
		elif line.find('max') != -1:
			type = 2
			print("es max")
		else:
			type = 0
			print("Error: Invalid problem")
		aux = file_to_matrix(line, type)
		file.close()
	except:
		aux = None
		print("No such file or directory: ", file_name)
	return aux

def file_to_matrix(line, type):
	decision = int(line[4])
	restrictions = int(line[6])
	matrix = np.zeros((restrictions+1, restrictions+decision+1))
	line = line[8:]
	line = line.split(',')
	line_aux = []
	for i in line:
		if i.find('\n') != -1:
			array = i.split('\n')
			line_aux.append(array[0])
			line_aux.append(array[1])
		else:
			line_aux.append(i)
		
	for i in range(decision):
		line_aux[i] = int(line_aux[i]) * -1
		
		
	l = 0
	k = 1
	flag = -1
	for i in range(restrictions+1):
		flag += 1
		k = 1
		for j in range(restrictions+decision+1):
			if j < decision:
				matrix[i][j] = line_aux[l]
				l += 1
			elif i == 0:
				matrix[i][j] = 0
			elif j == restrictions+decision:
				matrix[i][j] = line_aux[l]
				l += 2
			else:
				if k == flag:
					matrix[i][j] = 1
				k += 1
				
	return SimplexMethod(matrix, restrictions+1, restrictions+decision+1, decision, restrictions)

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", help= "Input file name")
	parser.add_argument("-o", "--output", help="Output file name")
	args = parser.parse_args()
	 
	if args.input:
		print("Entrada:", args.input)
		simplex = open_file(args.input)
		if simplex is None:
			print("es nulo")
		else:
			simplex.build_matrix()
			simplex.print_matrix()
	 
	if args.output:
		print("Salida:", args.output)
