import math
import numpy as np
from fractions import Fraction

class SimplexMethod(object):

	def __init__(self, matrix_aux, row_size, column_size, decision, restrictions, sign,flag, VB):
		self.matrix_aux = matrix_aux
		self.row_size = row_size
		self.column_size = column_size
		self.decision = decision
		self.restrictions = restrictions
		self.sign = sign
		self.start_VB(VB, decision, restrictions)
		self.flag = flag
		self.isDegenerate = False
		self.U_bounded = False
		self.multiple = -1

	def start_VB(self, VB, decision, restrictions):
		self.VB = [0]
		cont = decision + 1
		for i in self.sign:
			if i == "<=":
				self.VB.append(cont)
				cont += 1
			elif i == "=":
				self.VB.append(cont)
				cont += 1
			elif i == ">=":
				cont += 1
				self.VB.append(cont)
				cont += 1

	"""
		Convierte los elementos de la matriz en fracciones
	"""
	def build_matrix(self):
		# self.matrix = np.zeros((self.row_size, self.column_size))

		# for i in range(self.row_size):
		# for j in range(self.column_size):
		# self.matrix[i][j] = int(self.matrix_aux[i][j])\
		self.matrix = [0] * (self.row_size)
		for i in range(self.row_size):
			self.matrix[i] = [0] * self.column_size
		for i in range(self.row_size):
			for j in range(self.column_size):
				self.matrix[i][j] = self.matrix_aux[i][j]

	def print_matrix(self):
		M = 10000
		for p in range(self.column_size):
			print("-----------",end="")
		print()
		print(" VB ",end="")
		for p in range(self.column_size-1):
			print(" X-"+str(p+1)+"      ",end="")
		print("  R  ",end="")
		print('\n')
		for i in range(self.row_size):
			if(i==0):
				print(" U ",end="")
			else:
				print("X-" + str(self.VB[i]),end="")
			for j in range(self.column_size):
				if(i ==0):
					print(" | ",end="")
					if(int(self.matrix[i][j][0]) ==0 and (int(self.matrix[i][j][1])/M) == 0):
						print("0",end="")
					elif(int(self.matrix[i][j][0]) ==0):
						print(str((int(self.matrix[i][j][1])/M)) + 'M',end="")
					elif((int(self.matrix[i][j][1])) ==0):
						print(str(int(self.matrix[i][j][0])),end="")
					else:
						print(str(int(self.matrix[i][j][0])) +' + '+str((int(self.matrix[i][j][1])/M)) + 'M',end="")
					print(" | ",end="")
				else:
					print(" | ",end="")
					# print(int())
					print("%.2f" % (self.matrix[i][j]) ,end="")
					# print(int(self.matrix[i][j]),end="")
					print(" | ",end="")
			print('\n')
		# print(self.matrix)
	

	def get_result(self):
		if(self.flag==0):
			self.result = np.zeros(self.decision + self.restrictions + 1)
		else:
			self.result = np.zeros(self.decision + self.restrictions + 2)
		j = 0
		for i in self.VB:
			if(i==0):
				self.result[i] = self.matrix[j][self.column_size-1][0] +self.matrix[j][self.column_size-1][1]
			else:
				self.result[i] = self.matrix[j][self.column_size-1]
			j += 1

	"""
		Funcion controlador del metodo simplex
	"""
	def simplex(self, exitA):
		# print(salida)
		# archivo = open(salida, "w+")
		FileS= open(exitA, "w+")
		# print(self.matrix_aux)
		# archivo.write(str(self.matrix)+'\n')
		# self.imprimeArchivo(self.matrix, archivo)
		self.write_file(self.matrix, FileS)
		
		countV = 0
		while(self.check_matrix()):
			#verifica si la U es no acotada
			countV +=1
			if countV != 200:
				self.choose_column()
				#verifica si la U es no acotada
				if self.check_U():
					FileS.write("U no acotada")
					self.U_bounded = True
					break
				self.choose_pivot()
				self.new_matrix()
				# archivo.write(str(self.matrix)+'\n')
				# print("a")
				# guardarArchivo(self)
				FileS.write("Pivote: " + str(self.pivot[1]) +'\n')
				#print("Pivote: ", self.pivot[1])
				#print("Entra: X-", self.column + 1)
				FileS.write("Entra: X-" + str(self.column + 1) +'\n')
				#print("Sale: X-", self.VB[self.pivot[0]])
				FileS.write("Sale: X-" + str(self.VB[self.pivot[0]]) +'\n')
				self.VB[self.pivot[0]] = self.column + 1
				# print(self.VB)
				#print("----------------------------------------------------")
				# archivo.write(str(self.matrix)+'\n')
				self.write_file(self.matrix,FileS)
				if self.isDegenerate == False:
					self.check_degenerate()
			else:
				print("No tiene solucion")
				break
		self.get_result()
		self.SaveResult(FileS)
		if self.isDegenerate == True:
			FileS.write("Solucion optima degenerada")
		if self.check_multiple():
			FileS.write("Solucione multiple\n")
			print("multiple")
			self.column = self.multiple
			self.choose_pivot()
			self.new_matrix()
			FileS.write("Pivote: " + str(self.pivot[1]) +'\n')
			FileS.write("Entra: X-" + str(self.column + 1) +'\n')
			FileS.write("Sale: X-" + str(self.VB[self.pivot[0]]) +'\n')
			self.VB[self.pivot[0]] = self.column + 1
			# self.imprimeArchivo(self.matrix,archivo)
			self.write_file(self.matrix,FileS)
		FileS.close()
		
	def check_multiple(self):
		print(self.VB)
		for i in range(self.column_size):
			if i+1 not in self.VB:
				res = self.matrix[0][i][0] + self.matrix[0][i][1]
				if res == 0:
					self.multiple = i
					return True
		return False
		
	def check_degenerate(self):
		for i in range(1, self.row_size):
			if self.matrix[i][self.column_size-1] == 0:
				self.isDegenerate = True

	def check_U(self):
		U_bounded = True
		for i in range(self.row_size):
			if(i==0):
				res = self.matrix[i][self.column][0] + self.matrix[i][self.column][1]
				if(res>0):
					print("matriz: ", self.matrix[i][self.column])
					U_bounded = False
			else:				
				if self.matrix[i][self.column] > 0:
					print("matriz: ", self.matrix[i][self.column])
					U_bounded = False
		return U_bounded

	def print_result(self):
		print("U = ", self.result[0])
		for i in range(1, len(self.result)):
			print(len(self.result))
			print("X**", i, " = ", self.result[i])
		if self.isDegenerate == True:
			print("Solucion optima degenerada")
		if self.U_bounded:
			print("U no acotada")
	
	def write_file(self, matrix, fileA):
		M = 10000
		for p in range(self.column_size):
			fileA.write("-----------")
		fileA.write('\n')
		fileA.write(" VB ")
		for p in range(self.column_size-1):
			fileA.write(" X-"+str(p+1)+"      ")
		fileA.write("  R  ")
		fileA.write('\n')
		for i in range(self.row_size):
			if(i ==0):
				fileA.write(" U ")
			else:
				fileA.write("X-" + str(self.VB[i]))
			for j in range(self.column_size):
				if(i ==0):
					fileA.write(" | ")
					if(int(self.matrix[i][j][0]) ==0 and (int(self.matrix[i][j][1])/M) == 0):
						fileA.write("0")
					elif(int(self.matrix[i][j][0]) ==0):
						fileA.write(str((int(self.matrix[i][j][1])/M)) + 'M')
					elif((int(self.matrix[i][j][1])) ==0):
						fileA.write(str(int(self.matrix[i][j][0])))
					else:
						fileA.write(str(int(self.matrix[i][j][0])) +' + '+str((int(self.matrix[i][j][1])/M)) + 'M')
					fileA.write(" | ")
				else:
					fileA.write(" | ")
					# print(int())
					fileA.write("%.2f" % (self.matrix[i][j]))
					# print(int(self.matrix[i][j]),end="")
					fileA.write(" | ")
			fileA.write('\n')
		fileA.write('\n')
		# archivo.close()
	
	def SaveResult(self, fileP):
		fileP.write("U = " + str(self.result[0]))
		fileP.write('\n')
		for i in range(1, len(self.result)):
			fileP.write("X**" + str(i) + " = " + str(self.result[i]))
			fileP.write('\n')

	"""
		Selecciona la columna por la cual se empezara a trabajar
		Metodo para simplex
	"""
	def choose_column(self):
		res = self.matrix[0][0][0] + self.matrix[0][0][1]
		# bit = self.matrix[0][0]
		res2=0
		j = 0
		for i in range(1, self.column_size-1):
			res2 = self.matrix[0][i][0] + self.matrix[0][i][1]
			if res2 < res:
				# bit = self.matrix[0][i]
				res = res2
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
			if i ==0:
				auxA = self.matrix[i][self.column][0]*-1
				auxB = self.matrix[i][self.column][1]*-1
				for j in range(self.column_size):
					if i != self.pivot[0]:
						self.matrix[i][j][0] = self.matrix[i][j][0] + (auxA * self.matrix[self.pivot[0]][j])
						self.matrix[i][j][1] = self.matrix[i][j][1] + (auxB * self.matrix[self.pivot[0]][j])
			else:
				aux = self.matrix[i][self.column]*-1
				for j in range(self.column_size):
					if i != self.pivot[0]:
						self.matrix[i][j] = self.matrix[i][j] + (aux * self.matrix[self.pivot[0]][j])

	def check_matrix(self):
		res2 = 0
		for i in range(self.column_size-1):
			res2 = self.matrix[0][i][0] + self.matrix[0][i][1]
			if res2 < 0:
				return True
		return False
