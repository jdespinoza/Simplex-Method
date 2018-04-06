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
		checker = check(line)
		print("hola")
		aux = file_to_matrix(line, type)
		print("hola2")
		file.close()
	except:
		aux = None
		print("No such file or directory: ", file_name)
	return aux

def check(line):
	line2 = line.split(',')
	aux = []
	for i in line2:
		if i.find('\n') != -1:
			array = i.split('\n')
			aux.append(array[0])
			aux.append(array[1])
			
		else:
			aux.append(i)
	print(aux)
	
	return 0
	
def file_to_matrix(line, type):
	flag_igual = 0
	largo = 0
	line2 = line.split(',')
	element0 = line2[0].split('\n')
	element1= line2[1].split('\n')
	decision = int(element0[1])
	restrictions = int(element1[0])
	aux = []
	for i in line2:
		if i.find('\n') != -1:
			array = i.split('\n')
			aux.append(array[0])
			aux.append(array[1])
			
		else:
			aux.append(i)
	# matrix = np.zeros((restrictions+1, restrictions+decision+1))
	# line = line[8:]
	# line = line.split(',')
	line_aux = []
	# for i in line:
	# if i.find('\n') != -1:
	# array = i.split('\n')
	# line_aux.append(array[0])
	# line_aux.append(array[1])	
	# else:
	# line_aux.append(i)
	line_aux = aux[3:]
	for i in range(decision):
		if type == 2:
			line_aux[i] = int(line_aux[i]) * -1
	# print(line_aux)
	l = 0
	k = 1
	flag = -1
	sign = []
	cantidad = 1
	for i in line_aux:
		if i == '>=':
			flag_igual=1
			sign.append(i)
			cantidad+=1
		elif i == '<=' or i == '=':
			sign.append(i)
	if flag_igual == 1:
		largo = restrictions+decision+cantidad
	else:
		largo = restrictions+decision+cantidad
	# print(cantidad)
	# print(restrictions)
	# print(decision)
	# print(largo)
	matrix = np.zeros((restrictions+1, largo))
	for i in range(restrictions+1):	
		flag += 1
		k = 1
		# print("i" + str(i))
		for j in range(largo):	
			# print("j" + str(j))	
			if j < decision:
				matrix[i][j] = line_aux[l]
				l += 1
			elif i == 0:
				matrix[0][j] = 0
			elif j == largo-1 :
				matrix[i][j] = line_aux[l]
				l += 1
				# sign.(line_aux[l])
				l += 1
			else:
				if k == flag:
					# print(sign[i-1])
					if sign[i-1] == ">=":
						# print("entro")
						matrix[i][j] = -1
						# print("entro2")
						matrix[i][j+1] = 1
						k+=1
						flag += 1
					else:
						matrix[i][j] = 1
				k += 1
				
	# print(sign)
	M = 1	
	i = 0
	j= 0 + decision
	while(i<len(sign)):
		if sign[i] == '=':
			matrix[0][j] = 1*M
			j+=1
		elif sign[i] == '>=':
			matrix[0][j+1] = 1*M
			j+=2
		else:
			j+=1
		i+=1
				
	# print(matrix)
	for i in range(len(sign)):
		# print(i)
		if sign[i] == '=' or sign[i] == '>=':
			for j in range(largo):
					matrix[0][j] -= matrix[i+1][j]*M
	return SimplexMethod(matrix, restrictions+1,largo, decision, restrictions, sign,flag_igual)

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
				simplex.simplex("out_"+args.input)
				simplex.print_matrix()
				simplex.print_result()
				simplex.resolve_M_op("3M+3", "2M+5", "-1.5")
