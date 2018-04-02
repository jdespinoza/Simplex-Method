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
			type = 1
		elif line.find('max') != -1:
			type = 2
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
	flag_igual = 0
	largo = 0
	decision = int(line[4])
	restrictions = int(line[6])
	# matrix = np.zeros((restrictions+1, restrictions+decision+1))
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
	sign = []
	cantidad = 0
	for i in line_aux:
		if i == '>=':
			flag_igual=1
			sign.append(i)
			cantidad+=1
		elif i == '<=' or i == '=':
			sign.append(i)
	if flag_igual == 1:
		largo = restrictions+decision+((cantidad)*2)
	else:
		largo = restrictions+decision+1
	print(largo)
	matrix = np.zeros((restrictions+1, largo))
	
	# for p in range(largo):
	# if p < decision:
	# matrix[0][p] = line_aux[l]
	# print(matrix[0][p])
	# l += 1
	# else:
	# matrix[0][p] = 0
	# print(matrix[0][p])

	for i in range(restrictions+1):	
		flag += 1
		k = 1
		print("algo2")
		for j in range(largo):
			print("algo")			
			if j < decision:
				matrix[i][j] = line_aux[l]
				l += 1
			elif i == 0:
				matrix[0][j] = 0
			elif j == restrictions+decision:
				matrix[i][j] = line_aux[l]
				l += 1
				# sign.(line_aux[l])
				l += 1
			else:
				if k == flag:
					if flag_igual ==1:
						matriz[i][j] = -1
						matriz[i][j+1] = 1
					else:
						matrix[i][j] = 1
				k += 1
				
	print(sign)
	M = 2		
	for i in range(len(sign)):
		# print(i)
		j = (i+decision)
		print(j)
		if sign[i] == '=' or sign[i] == '>=':
			if type ==2:
				matrix[0][j] = 1*M
	
	for i in range(len(sign)):
		# print(i)
		if sign[i] == '=' or sign[i] == '>=':
			for j in range(largo):
				if type ==2:
					matrix[0][j] -= matrix[i+1][j]*M
	# print(sign)
	print(matrix)

	# return SimplexMethod(matrix, restrictions+1,largo, decision, restrictions, sign)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", help= "Input file name")
	parser.add_argument("-o", "--output", help="Output file name")
	args = parser.parse_args()

	if args.input:
		print("Input FIle:", args.input)
		simplex = open_file(args.input)
		if simplex is None:
			print("Error: Simplex is None")
		else:
			if args.output:
				simplex.build_matrix()
				simplex.simplex(args.output)
				simplex.print_matrix()
				simplex.print_result()
			else:
				simplex.build_matrix()
				simplex.simplex("salida.txt")
				simplex.print_matrix()
				simplex.print_result()
