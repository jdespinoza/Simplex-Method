import math
import numpy as np
from fractions import Fraction

class SimplexMethod(object):

	def __init__(self, matrix_aux, row_size, column_size, decision, restrictions, sign, flag):
		self.matrix_aux = matrix_aux
		self.row_size = row_size
		self.column_size = column_size
		self.decision = decision
		self.restrictions = restrictions
		self.sign = sign
		self.start_VB(decision, restrictions)

	def start_VB(self, decision, restrictions):
		self.VB = [0]
		for i in range(decision+1, 1000):
			if restrictions <= 0:
				break
			self.VB.append(i)
			restrictions -= 1

	"""
		Convierte los elementos de la matriz en fracciones
	"""
	def build_matrix(self):
		self.matrix = np.zeros((self.row_size, self.column_size))

		for i in range(self.row_size):
			for j in range(self.column_size):
				self.matrix[i][j] = str(self.matrix_aux[i][j])

	def print_matrix(self):
		print(self.matrix)

	def get_result(self):
		self.result = np.zeros(self.decision + self.restrictions + 1)
		j = 0
		for i in self.VB:
			self.result[i] = self.matrix[j][self.column_size-1]
			j += 1



	"""
		Funcion controlador del metodo simplex
	"""
	def simplex(self, salida):
		archivo = open(salida, "w+")
		while(self.check_matrix()):
			self.choose_column()
			self.choose_pivot()
			self.new_matrix()
			archivo.write(str(self.matrix)+'\n')
			archivo.write("Pivote: " + str(self.pivot[1]) +'\n')
			#print("Pivote: ", self.pivot[1])
			#print("Entra: X-", self.column + 1)
			archivo.write("Entra: X-" + str(self.column + 1) +'\n')
			#print("Sale: X-", self.VB[self.pivot[0]])
			archivo.write("Sale: X-" + str(self.VB[self.pivot[0]]) +'\n')
			self.VB[self.pivot[0]] = self.column + 1
			#print(self.VB)
			#print("----------------------------------------------------")
		self.get_result()
		archivo.close()

	def print_result(self):
		print("U = ", self.result[0])
		for i in range(1, len(self.result)):
			print("X**", i, " = ", self.result[i])

	"""
		Selecciona la columna por la cual se empezara a trabajar
		Metodo para simplex
	"""
	def choose_column(self):
		bit = self.matrix[0][0]
		j = 0
		for i in range(1, self.column_size-1):
			if self.matrix[0][i] < bit:
				bit = self.matrix[0][i]
				j = i
		self.column = j

	"""
		Selecciona el pivote de acuerdo a la columna seleccionada
	"""
	def choose_pivot(self):
		bit = self.choose_pivot_aux(self.matrix[1][self.column], self.matrix[1][self.column_size-1])
		j = 1
		pivot_number = self.matrix[1][self.column]
		for i in range(2, self.row_size):
			bit_aux = self.choose_pivot_aux(self.matrix[i][self.column], self.matrix[i][self.column_size-1])
			if bit_aux < bit:
				bit = bit_aux
				j = i
				pivot_number = self.matrix[i][self.column]
		self.pivot = [j, pivot_number]

	"""
		Evita divisiones entre cero
	"""
	def choose_pivot_aux(self, num1, num2):
		if num1 <= 0:
			return 10000
		try:
			result = num2 / num1
		except:
			result = 0

		return result

	def new_matrix(self):
		for i in range(self.column_size):
			self.matrix[self.pivot[0]][i] /= self.pivot[1]

		for i in range(self.row_size):
			self.aux = self.matrix[i][self.column]*-1
			for j in range(self.column_size):
				if i != self.pivot[0]:
					self.matrix[i][j] = self.matrix[i][j] + (self.aux * self.matrix[self.pivot[0]][j])

	def check_matrix(self):
		for i in range(self.column_size):
			if self.matrix[0][i] < 0:
				return True
		return False
		
	def resolve_M_op(self, op1, op2, aux):
		#validar si no tiene M
		mul = self.split_M(aux)
		
		if op1.find('M') != -1 and mul.find('M') != -1:
			type_M = 1
		elif op1.find('M') != -1 and op2.find('M') != -1:
			type_M = 2
		elif op1.find('M') != -1:
			type_M = 3
		elif op2.find('M') != -1:
			type_M = 4
		elif mul.find('M') != -1:
			type_M = 5
		else:
			type_M = 6
		result = []
		op1 = self.split_M(op1)
		op2 = self.split_M(op2)
		
		if type_M == 1:
			aux1 = str(float(op2) * float(mul[0][0:-1]))
			aux1 = aux1 + 'M'
			aux2 = str(float(op2) * float(mul[1]))
			op2 = []
			op2.append(aux1)
			op2.append(aux2)
			result.append(str(float(op1[0][:-1])+float(op2[0][:-1])))
			if float(result[0]) > 0:
				result[0] = result[0]+'M'
			else:
				result = []
			result.append(str(float(op1[1])+float(op2[1])))
			result = self.toString_M(result)
			print(result)
		elif type_M == 2:
			op2[0] = str(float(op2[0][0:-1]) * float(mul))
			op2[0] = op2[0] + 'M'
			op2[1] = str(float(op2[1]) * float(mul))
			result.append(str(float(op1[0][:-1])+float(op2[0][:-1])))
			if float(result[0]) > 0:
				result[0] = result[0]+'M'
			else:
				result = []
			result.append(str(float(op1[1])+float(op2[1])))
			result = self.toString_M(result)
			print(result)
		elif type_M == 3:
			op2 = str(float(op2)*float(mul))
			result.append(str(op1[0]))
			result.append(str(float(op1[1])+float(op2)))
			result = self.toString_M(result)
			print(result)
		elif type_M == 4:
			op2[0] = str(float(op2[0][0:-1]) * float(mul))
			op2[0] = op2[0] + 'M'
			op2[1] = str(float(op2[1]) * float(mul))
			result.append(op2[0])
			result.append(str(float(op1)+float(op2[1])))
			result = self.toString_M(result)
			print(result)
		elif type_M == 5:
			aux1 = str(float(op2) * float(mul[0][0:-1]))
			aux1 = aux1 + 'M'
			aux2 = str(float(op2) * float(mul[1]))
			op2 = []
			op2.append(aux1)
			op2.append(aux2)
			result.append(op2[0])
			result.append(str(float(op2[1])+float(op1)))
			result = self.toString_M(result)
			print(result)
		else:
			result = str(float(op1) + (float(op2) * float(mul)))
			print(result)
			
	def split_M(self, num):
		if num.find('+') != -1:
			num = num.split('+')
			num.append('+')
		elif num.find('-') != -1:
			aux = num.split('-')
			if len(aux[0]) != 0:
				aux.append('-')
				num = aux
		return num
		
	def toString_M(self, array):
		number = ""
		for i in array:
			number += i
			
		return number
