#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import numpy as np

from SimplexMethod import SimplexMethod

"""
	lee el archivo y separa los valores leidos, y verifica si es max o min
	tambien indica al usuario si el formato del archivo es erroneo
"""
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
		checker = check(file_name,line)
		if(checker == 0): 
			aux = file_to_matrix(line, type)
			file.close()
			return aux
		else:
			print("Error: FIle, Invalid problem")
		file.close()
	except:
		aux = None
		print("No such file or directory: ", file_name)
	return None

"""
Funcion que revisa el archivo y valida si
son numeros, sin letras y que tenga el tamano 
que debe de tener
"""		
def check(file_name,line3):
	file = open(file_name, "r")
	line4 = line3.split(',')
	aux = []
	for i in line4:
		if i.find('\n') != -1:
			array = i.split('\n')
			aux.append(array[0])
			aux.append(array[1])
		else:
			aux.append(i)
	line = file.readline()
	element = line.split('\n')
	if(element[0] == 'max' or element[0] == 'min'):
		line = file.readline()
		line2 = line.split(',')
		if(len(line2) == 2):
			element2= line2[1].split('\n')
			if(line2[0].isdigit() and element2[0].isdigit()):
				var = int(line2[0])
				res = int(element2[0])
				total = 3 + var + ((var+2)*res)+1
				if(total != len(aux)):
					return 1
				line = file.readline()
				line2 = line.split(',')
				if(len(line2) == var):
					i = 0
					while(i<var):
						if(i == (var-1)):
							element2= line2[i].split('\n')
							try:
								valor = int(element2[0])
							except ValueError:
								return 1
					
						else:
							# if(line2[i].isdigit() == False):
							# return 1
							try:
								valor = int(line2[i])
							except ValueError:
								return 1
				
						i+=1
					i = 0
					while(i<res):
						line = file.readline()
						line2 = line.split(',')
						j =0
						if(len(line2) ==(var+2)):
					
							while(j<(var+2)):
								if(j==(var+1)):
									element = line2[j].split('\n')
									if(element[0] != '=' and element[0] != '<=' and element[0] != '>='):
										return 1
										
							
								else:
									# if(line2[j].isdigit() == False):
									# return 1
									try:
										valor = int(line2[j])
									except ValueError:
										return 1
								j+=1
							
						else:
							return 1
							
						i+=1
					
				else:
					return 1	
			else:
				return 1
		else:
			return 1
	else:
		return 1
	file.close()
	return 0
	
"""
	Coloca los valores leidos del archivo en una matriz,
	a esta matriz se le ira insertando las variables de holgura,
	exceso y artificiales segun corresponda, tambien se incluyen
	las M a los valores que lo necesiten
"""
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
	line_aux = aux[3:]
	for i in range(decision):
		if type == 2:
			line_aux[i] = int(line_aux[i]) * -1
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
	#matrix = np.zeros((restrictions+1, largo))
	matrix = [0] * (restrictions+1) 
	VB = []
	
	for i in range(restrictions+1):
		matrix[i] = [0] * largo
	"""
	llena la matrix, con los datos del archivo
	"""
	for i in range(restrictions+1):	
		flag += 1
		k = 1
		for j in range(largo):	
			if j < decision:
				matrix[i][j] = int(line_aux[l])
				l += 1
			elif i == 0:
				matrix[0][j] = 0
			elif j == largo-1 :
				matrix[i][j] = int(line_aux[l])
				l += 1
				# sign.(line_aux[l])
				l += 1
			else:
				if k == flag:
					# print(sign[i-1])
					if sign[i-1] == ">=":
						matrix[i][j] = -1
						matrix[i][j+1] = 1
						k+=1
						flag += 1
						VB.append(j+2)
					else:
						matrix[i][j] = 1
				k += 1
				
	M = 10000
	i = 0
	j= 0 + decision
	# print(matrix)
	for p in range(largo):
		matrix[0][p] = [matrix[0][p],0]
	"""
	agrega la M a la matriz
	"""	
	while(i<len(sign)):
		if sign[i] == '=':
			#matrix[0][j] = 1*M
			matrix[0][j] = [matrix[0][j][0],M]
			j+=1
		elif sign[i] == '>=':
			if type ==1:
				#matrix[0][j+1] = 1*M
				matrix[0][j+1]= [matrix[0][j+1][0],M]
			else:
				#matrix[0][j+1] = 1*M
				matrix[0][j+1]= [matrix[0][j+1][0],M]
			j+=2
		else:
			j+=1
		i+=1
				
	# print(matrix)
	"""
	modifica la u, para tener el valor de la fila
	y eliminar las artificiales, en la fila u
	"""
	for i in range(len(sign)):
		# print(i)
		if sign[i] == '=' or sign[i] == '>=':
			for j in range(largo):
					#matrix[0][j] -= matrix[i+1][j]*M
					matrix[0][j][1] -= matrix[i+1][j]*M
	# print(sign)
	# print(matrix)

	return SimplexMethod(matrix, restrictions+1,largo, decision, restrictions, sign,flag_igual, VB)

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
