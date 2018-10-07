#NAME & ROLL.NO = {"ASHUTOSH BANSAL":"2017140","KANISHK RANA":"2017241","RAHUL MADAAN":"2017179","SHAURYA BAGGA":"2017104"}
#SECTION B
from copy import copy
import math
from string import ascii_uppercase as au
class minterms:
	"""this class defines the minterms,sorts them in the list, converts them to binary for which i have used two functions """
	def __init__(self,list,dontCares=[]):
		self.minterm = list
		self.minterm.sort()
		self.dontCares= dontCares
		self.dontCares.sort()
	@staticmethod
	def decimalTobinary(a):
		""" this functions just divides the number (minterm) by 2 and gives the binary output in reverse way for eg. decimalTobinary(4) will give 001. the next function invers this output to give the actual binary representation that is 100."""
		t = ''
		if a == 0:
			t = "0"
			return t
		elif a == 1:
			t+="1"
			return t
		elif (a % 2 != 0):
			t+="1"
			b = a//2
		else:
			t+="0"
			b = a/2
		t = t + minterms.decimalTobinary(b)
		return t
	@staticmethod
	def binaryConversion(a):
		t = minterms.decimalTobinary(a)
		d = []
		for i in t:
			d.append(i)
		for i in range(len(t)):
			if t[i]=="1":
				d[i],d[len(t)-1-i]=d[len(t)-1-i],d[i]
			else:
				continue
		b = ''
		for i in d:
			b+=str(i)
		return b
class termTable(minterms):
	""" this class inherits from the class minterms. the function table makes a list of the minterms in their binary form. and the function mintermTable gives a pretty representation i.e. will give the minterms with all equal number of bits."""
	def __init__(self,minterm,dontCares=[]):
		super().__init__(minterm,dontCares=[])
	
	def table(self):
		table = []
		for i in self.minterm :
			table.append(super().binaryConversion(i))
		return table
	
	def mintermTable(self):
		C = self.table()
		A = len(C[-1])
		for i in range(len(C)-1):
			if len(C[i])<A:
				B = abs(len(C[i]) - A)
				C[i] = B*'0' + C[i]
			else:
				pass
		return C
	def link(self):
		""" this function creates a dictionary that has binary values as its keys and its decimal equivalent as values. """
		d = {}
		C = self.mintermTable()
		A = self.minterm
		for i in range(len(A)):
			d[C[i]]=A[i]
		return d
	def DividedTables(self):
		""" this function creates a list wherein the binary numbers corresponding to the minterms are seperated on the basis of no. of '1's in them. for eg. '0001' will be in the key Count1, '0011' will be in the key Count2. """
		A = self.mintermTable()
		maximum = len(A[-1])
		#print (maximum)
		d = {}
		for i in range(maximum+1):
			d["Count"+str(i)]=[]
		#print (d)
		for i in range(maximum+1):
			for j in range(len(A)):
				if A[j].count("1") == i:
					#print (A[j],i)
					d["Count"+str(i)].append(A[j])
				else:
					pass
		return d
class primeImplicants(termTable):
	""" this class has been inherited from termTable. the function match is actually logical XOR function which checks between two bits of two minterms simultaneously"""
	def __init__(self,minterm,dontCares=[]):
		super().__init__(minterm,dontCares=[])
	@staticmethod
	def match(a,b):
		count = 0
		for i in range(len(a)):
			if a[i]==b[i]:
				continue
			elif a[i]!=b[i]:
				count +=1
		if count == 1:
			index = 0
			for i in range(len(a)):
				if a[i]==b[i]:
					continue
				elif a[i]!=b[i]:
					index = i
			return True, a[:index]+'-'+a[index+1:]
		else:
			return False,None
	def give_prime_implicants(self):
		"""this function clubs 2 minterms together, the next function clubs minterms upto the exten they can"""
		A = self.DividedTables()
		B = self.link()
		C = []
		D = []
		for i in range(len(A)-1):
			for j in A["Count"+str(i)]: #for clubbing 2 minterms together we need to MATCH minterms from adjacent COUNT's as only they will differ in 1 bit
				for k in A["Count"+str(i+1)]:
					E,F = primeImplicants.match(j,k)
					if E == True:
						C.append([B[j],B[k]])
						D.append(F)
		for i in B:
			count = 0
			for j in range(len(D)):
				if B[i] not in C[j]:
					count+=1
			if count == len(C):
				C.append([B[i]])
				D.append(i)
		E = {} # creating 2 dictionaries which store the minterms that were clubbed together and also those which coouldn't be clubbed together, the second dictionary just stores the resultant binary value of the same. the key of the dictionary has been set in such a way that clubbing 2 minterms is the value of E0, clubbing 4 minterms is the value of E1, 8 of E2 and so on. same is with F.
		F = {}
		x = 0
		
		for i in range(len(A)):
			if len(A["Count"+str(i)])!=0:
				x = i
				break
		for i in range(len(A["Count" + str(x)][0])):
			E['E'+str(i)]=[]
			F['F'+str(i)]=[]
		E['E0']=C
		F['F0']=D
		return E,F

	@staticmethod
	def unique(A):
		indexes = [i for i in range(len(A))]
		for g in range(len(A)-1):
			for h in range(g+1,len(A)):
				a = list(A[g])
				b = list(A[h])
				a.sort()
				b.sort()
				if a == b:
					indexes.remove(h)
					break
		A = [A[i] for i in indexes]
		return A,indexes
	def lets_recurse_using_loops(self):
		"""this function implements the rest of the clubbing, by going in every entry of the dictionary F and matches with every other possible entry."""
		E,F = self.give_prime_implicants()
		for i in range(1,len(E)):
			for j in range(len(F["F"+str(i-1)])):
				for k in range(j+1,len(F["F"+str(i-1)])):
					A,B = primeImplicants.match(F["F"+str(i-1)][j],F["F"+str(i-1)][k])
					if A == True:
						F["F"+str(i)].append(B)
						X = list(E["E"+str(i-1)][j]) # a shallow copy is created else changes in this list will lead to changes in the original list itself.
						Y = list(E["E"+str(i-1)][k]) # this just appends the clubbed minterms in the dictionary E. (clubbing takes place in repective keys, i.e. clubbing of 4 in E1, of 8 in E2, of 16 in E3 etc.)
						X.extend(Y)
						E["E"+str(i)].append(X)
			#print (E,F)

		X = []   # the following code removes the clubbing of the minterms that have been clubbed further i.e. if a 2,2 clubbings are there in E0 which form a bigger clubbing in E1, then remove the clubbings from E0.
		for i in range(1,len(E)):
			for g in range(len(E["E"+str(i)])):
				for j in range(len(E["E"+str(i-1)])):
					count = 0
					for h in range(len(E["E"+str(i-1)][j])):
						if E["E"+str(i-1)][j][h] in E["E"+str(i)][g]:
							count +=1
					if count == len(E["E"+str(i-1)][j]):
						X.append(list(E["E"+str(i-1)][j]))
		
		for i in range(len(X)):
			x = math.log(len(X[i]),2)
			x = int(x)
			index = 0
			for j in range(len(E["E"+str(x-1)])):
				if X[i] == E["E"+str(x-1)][j]:
					index = j
			E["E"+str(x-1)][index]=[]
			F["F"+str(x-1)][index]="1"
		#print (E,F)
		    # the following lines create two new dictionaries, with only the unique minterms i.e. without repititions.
		F1={}
		for i in F:
			F1[i]=[]
		for i in range(len(E)):
			E["E"+str(i)],j = primeImplicants.unique(E["E"+str(i)])
			for g in j:
				F1["F"+str(i)].append(F["F"+str(i)][g])
			
		return (E,F1)

			


class eprimeImplicants(primeImplicants):
	"""this class has been inherited from primeImplicants class. the following functions give the representation of the output by selecting the dont cares."""
	def __init__(self,minterm,dontCares=[]):
		super().__init__(minterm,dontCares=[])
	def representation(A):
		t = ''
		y = au
		for i in range(len(A)):
			if A == "-"*len(A):
				return "1"
			elif A[i] == "1":
				t+=au[i]
			elif A[i] == "0":
				t+=au[i]+"'"
			elif A[i] == "-":
				continue
		return t
	def final(A):
		"""this functions takes care of the fact that no output is being repeated"""
		y = [] 
		count = {}	

		for i in range(len(A)):
			count[A[i]]=1
			for j in range(i+1,len(A)):
				if A[j]==A[i]:
					count[A[i]] +=1
		for i in count:
			if count[i] == 1:
				y.append(i)
		return y


	def give_eprime_implicants(self):
		"""this function takes in the prime implicants, count the occurences of minterms, and then selects those minterms which occur once and prints them using the functions that are defined above."""
		E,F = self.lets_recurse_using_loops()
		D = {}
		for i in self.minterm:
			D[i] = 0
		for i in E:
			for j in range(len(E[i])):
				for k in range(len(E[i][j])):
					D[E[i][j][k]]+=1

		x = []
		for i in D:
			if D[i]==1:
				#print ("i",i)
				for j in range(len(E)):
					#print ("j",j)
					for k in range(len(E["E"+str(j)])):
						#print ("k",k)
						for l in range(len(E["E"+str(j)][k])):
							#print ("l",l)
							if E["E"+str(j)][k][l] == i:
								#print ("hello",E["E"+str(j)][k][l])
								x.append(eprimeImplicants.representation(F["F"+str(j)][k]))
		
		x = eprimeImplicants.final(x)
		y = ''
		for i in x:
			y = y + i+" + "
		y = y[:-3]
		return y

a = [0,1,2,3,4,5,6,7,8,9,10]
A = minterms(a)
#print (A.minterm)
#print (A.minterm)
A1 = termTable(a)
#print (A1.minterm)
#print (A1.link())
#print (A1.table())

#print (A1.link())
#print (A1.DividedTables())

A2 = primeImplicants(a)
#print (A2.give_prime_implicants())
#print (A2.lets_recurse_using_loops())
A3 = eprimeImplicants(a)
print (A3.give_eprime_implicants())
#help(eprimeImplicants)

