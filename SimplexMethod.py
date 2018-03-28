import math
import numpy as np
from fractions import Fraction

class SimplexMethod(object):
	
	def __init__(self, matrix_aux, row_size, column_size, decision, restrictions, sign):
		self.matrix_aux = matrix_aux
		self.row_size = row_size
		self.column_size = column_size
		self.decision = decision
		self.restrictions = restrictions
		self.sign = sign
		
	"""
		Convierte los elementos de la matriz en fracciones
	"""
	def build_matrix(self):
		self.matrix = np.zeros((self.row_size, self.column_size))
		
		for i in range(self.row_size):
			for j in range(self.column_size):
				self.matrix[i][j] = Fraction(self.matrix_aux[i][j])
				
	def print_matrix(self):
		print(self.matrix)
		
	"""
		Funcion controlador del metodo simplex
	"""
	def simplex(self):
		self.choose_column()
		self.choose_pivot()
		
	"""
		Selecciona la columna por la cual se empezara a trabajar
		Metodo para simplex
	"""
	def choose_column(self):
		bit = self.matrix[0][0]
		j = 0
		for i in range(1, self.column_size):
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
		for i in range(2, self.row_size):
			bit_aux = self.choose_pivot_aux(self.matrix[i][self.column], self.matrix[i][self.column_size-1])
			if bit_aux < bit:
				bit = bit_aux
				j = i				
		self.pivot = [j, bit]
		
	"""
		Evita divisiones entre cero
	"""
	def choose_pivot_aux(self, num1, num2):
		try:
			result = num2 / num1
		except:
			result = 0
			
		return result
			
	def new_matrix(self):
		
			
			
			
			
