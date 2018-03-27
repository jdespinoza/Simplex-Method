import math
import numpy as np
from fractions import Fraction

class SimplexMethod(object):
	def __init__(self, matrix_aux, row_size, column_size, decision, restrictions):
		self.matrix_aux = matrix_aux
		self.row_size = row_size
		self.column_size = column_size
		self.decision = decision
		self.restrictions = restrictions
		
	def build_matrix(self):
		self.matrix = np.zeros((self.row_size, self.column_size))
		
		for i in range(self.row_size):
			for j in range(self.column_size):
				self.matrix[i][j] = Fraction(self.matrix_aux[i][j])
				
	def print_matrix(self):
		print(self.matrix)
