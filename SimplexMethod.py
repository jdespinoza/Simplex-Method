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
		#iniciacion de las VB
		self.start_VB(VB, decision, restrictions)
		#banderas
		self.flag = flag
		self.isDegenerate = False
		self.U_bounded = False
		self.multiple = -1

	"""
		Se inicializan las VB de acuerdo a los signos
		del problemas (<=, >=, =)
	"""
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
				#se ignora la de exceso
				cont += 1
				self.VB.append(cont)
				cont += 1

	"""
		Copiamos la matrix de parametro a la matrix de la clase
		para evitar cualquier incoveniente con el tipo de dato
	"""
	def build_matrix(self):
		self.matrix = [0] * (self.row_size)
		for i in range(self.row_size):
			self.matrix[i] = [0] * self.column_size
		for i in range(self.row_size):
			for j in range(self.column_size):
				self.matrix[i][j] = self.matrix_aux[i][j]

	"""
		Imprime de forma entendible la matriz con sus
		respectivas VB
	"""
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
					print("%.2f" % (self.matrix[i][j]) ,end="")
					print(" | ",end="")
			print('\n')

	"""
		Crea un arreglo con los valores de las VB y de la U
	"""
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
		Maneja el ciclo principal del metodo simplex
	"""
	def simplex(self, exitA):
		FileS= open(exitA, "w+")
		self.write_file(self.matrix, FileS)
		countV = 0
		
		while(self.check_matrix()):
			countV +=1
			if countV != 200:
				self.choose_column()
				#verifica si la U es no acotada
				if self.check_U():
					FileS.write("U no acotada\n")
					self.U_bounded = True
					break
				self.choose_pivot()
				self.new_matrix()
				#escribe en archvo el pivote y las variables que salen y entran
				FileS.write("Pivote: " + str(self.pivot[1]) +'\n')
				FileS.write("Entra: X-" + str(self.column + 1) +'\n')
				FileS.write("Sale: X-" + str(self.VB[self.pivot[0]]) +'\n')
				#intercambia los valores de las VB
				#los que salen y los que entran
				self.VB[self.pivot[0]] = self.column + 1
				self.write_file(self.matrix,FileS)
				#verifica si la matrix actual es degenerada o no
				if self.isDegenerate == False:
					self.check_degenerate()
			else:
				print("No tiene solucion")
				break
		self.get_result()
		self.SaveResult(FileS)
		#verifica las banderas para indicar al usuario el estado de la solucion
		if self.isDegenerate:
			FileS.write("Solucion optima degenerada")
		#si es solucion multiple se hace una iteracion mas
		if self.check_multiple():
			self.print_matrix()
			self.print_result()
			FileS.write("Solucione multiple\n")
			print("Solucion Multiple")
			self.column = self.multiple
			self.choose_pivot()
			self.new_matrix()
			FileS.write("Pivote: " + str(self.pivot[1]) +'\n')
			FileS.write("Entra: X-" + str(self.column + 1) +'\n')
			FileS.write("Sale: X-" + str(self.VB[self.pivot[0]]) +'\n')
			self.VB[self.pivot[0]] = self.column + 1
			self.write_file(self.matrix,FileS)
			self.get_result()
			self.SaveResult(FileS)
		FileS.close()
		
	"""
		Verifica si una solucion tiene 0 en una variable
		no basica, si es asi, se activa bandera de solucion
		multiple
	"""
	def check_multiple(self):
		for i in range(self.column_size):
			if i+1 not in self.VB:
				res = self.matrix[0][i][0] + self.matrix[0][i][1]
				if res == 0:
					self.multiple = i
					return True
		return False
		
	"""
		Verifica si hay un 0 en la columna de respuestas
		si es asi, se activa bandera de degenerada
	"""
	def check_degenerate(self):
		for i in range(1, self.row_size):
			if self.matrix[i][self.column_size-1] == 0:
				self.isDegenerate = True

	"""
		Verifica si todos los coeficientes de la columna pivote 
		son negativos o cero
	"""
	def check_U(self):
		U_bounded = True
		for i in range(self.row_size):
			if(i==0):
				res = self.matrix[i][self.column][0] + self.matrix[i][self.column][1]
				if(res>0):
					U_bounded = False
			else:				
				if self.matrix[i][self.column] > 0:
					U_bounded = False
		return U_bounded

	"""
		Imprime los valores de U y de las VB
		ademas imprime si es degenerada o acotada
	"""
	def print_result(self):
		print("U = ", self.result[0])
		for i in range(1, len(self.result)):
			print("X**", i, " = ", self.result[i])
		if self.isDegenerate == True:
			print("Solucion optima degenerada")
		if self.U_bounded:
			print("U no acotada")
	
	"""
		Escribe en el archivo la matriz con sus respuestas
	"""
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
					fileA.write("%.2f" % (self.matrix[i][j]))
					fileA.write(" | ")
			fileA.write('\n')
		fileA.write('\n')
	
	"""
	Guarda la solucion, en el archivo
	"""
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
		res2=0
		j = 0
		for i in range(1, self.column_size-1):
			res2 = self.matrix[0][i][0] + self.matrix[0][i][1]
			if res2 < res:
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

	"""
		Genera una nueva matriz para una iteracion,
		se toma el valor que se encuentra en la columna pivote de la fila
		que se desea cambiar y se multiplica por -1
		luego a ese valor se le multiplica el valor de la columna de la fila
		pivote y se suma al valor que estoy cambiando
	"""
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
	
	"""
		Revisa si la matrix actual es una solucion optima
	"""
	def check_matrix(self):
		res2 = 0
		for i in range(self.column_size-1):
			res2 = self.matrix[0][i][0] + self.matrix[0][i][1]
			if res2 < 0:
				return True
		return False
