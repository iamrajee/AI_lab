#genetic algorithm
#in genotypic representation of real numbers,first position is reserved for sign, fouth position is reserved for decimal point,and other places are occupied by 0s and 1s, similar to actual representation of fractional binary number

import random
import string
import math
import numpy as np
import matplotlib.pyplot as plt

genes="01"
length=10

#function to convert binary string to float
def bintoflo(string):
	n=float(string)
	n1=int(n)
	n2=n%1
	n2=int(n2*1000000)
	string1=str(n1)
	n1=int(string1,2)
	string2=str(n2)
	p=2
	n2=0
	for i in range(len(string2)):
		n2=n2+(int(string2,10)/p)
		p=p*2
	n=n1+(0.1*n2)
	n=n-(n%0.01)
	return n

#function to convert float to binary string
def flotobin(n):
	string=[]
	string1=[]
	n1=int(n)
	n2=n%1
	c=0
	while(n1>0):
		r=n1%2
		string.append(str(r))
		n1=n1/2
		c+=1
	i=c-1
	while(i>=0):
		string1.append(string[i])
		i-=1
	string1.append('.')
	for i in range(6):
		n2=n2*2
		n3=int(n2)
		string1.append(str(n3))
		n2=n2%1
	string1="".join(string1)
	return string1	
	
#function to populate initial population
def populate(n):
	while True:
		string=[]
		string.append(random.choice("+-"))
		for i in range(1,10):
			if(i==3):
				string.append('.')
			else:
				string.append(random.choice(genes))
		string="".join(string)	
		n=bintoflo(string)
		if(n<=2.04 and n>=-2.04):
			break
	return string

#function to find pereto optimality and select individuals according best pereto optimality
def fitness(population,n):
	string=population[0]
	f1=0
	f2=0
	f3=0
	for i in range(5):
		n = bintoflo(string[i])
		f1=f1 + (n*n)
		f2=f2 + math.floor(n)
		f3=f3 + ((i+1)*n*n*n*n)
	f3 = f3 + np.random.normal(0,1)
	string1=population[1]
	h1=0
	h2=0
	h3=0
	for i in range(5):
		n = bintoflo(string[i])
		h1=h1 + (n*n)
		h2=h2 + math.floor(n)
		h3=h3 + ((i+1)*n*n*n*n)
	h3 = h3 + np.random.normal(0,1)
	if(f1<=h1 and f2<=h2 and f3<=h3):
		if(f1<h1 or f2<h2 or f3<h3):
			population1=[string,string1]
			f_value=[[f1,f2,f3],[h1,h2,h3]]
	else:
		population1=[string1,string]
		f_value=[[h1,h2,h3],[f1,f2,f3]]
	for j in range(2,int(n)):
		string=population[j]
		f1=0
		f2=0
		f3=0
		for i in range(5):
			n = bintoflo(string[i])
			f1=f1 + (n*n)
			f2=f2 + math.floor(n)
			f3=f3 + ((i+1)*n*n*n*n)
		f3 = f3 + np.random.normal(0,1)
		if(f1<=f_value[0][0] and f2<=f_value[0][1] and f3<=f_value[0][2]):
			if(f1<f_value[0][0] or f2<f_value[0][1] or f3<f_value[0][2]):
				population1[1]=population1[0]
				population1[0]=string
				f_value[1]=f_value[0]
				f_value[0]=[f1,f2,f3]
		elif(f1<=f_value[1][0] and f2<=f_value[1][1] and f3<=f_value[1][2]):
			if(f1<f_value[1][0] or f2<f_value[1][1] or f3<f_value[1][2]):
				population1[1]=string
				f_value[1]=[f1,f2,f3]
	return population1,f_value[0]


#mutation function
def mutation():
	string=''.join(random.choice(genes) for _ in range(1))
	return string

#crossover function
def crossover(string1, string2, n):
	while True:
		child=[]
		for i in range(10):
			if(i==0):
				prob =random.random()
				if(prob<0.5):
					child.append(string1[i])
				else:
					child.append(string2[i])
			elif(i==3):
				child.append('.')
			else:
				prob = random.random()
				if(prob < 0.7 ):
					child.append(string1[i])
				elif(prob < 0.9 ):
					child.append(string2[i])
				else:
					child.append(mutation())
		child=''.join(child)
		n=bintoflo(child)
		if(n<=2.04 and n>=-2.04):
			break
	return child

#genetic algorithm
def ga():
	popu_size=[50,100,200]
	for k in  range(3):
		iteration=[10,20,50,100,200,500]
		for b in range(6):
			iter_value=iteration[b]
			population_size=popu_size[k]
			population=[]
			for i in range(population_size):
				string=[]
				for j in range(5):
					string.append(populate(length))
				population.append(string)
			generation=1

			
		
			plot=[]
			
			for i in range (iter_value):
				population,plot1=fitness(population,population_size)
				plot.append(plot1)
				new_gen=[]
				for j in range(population_size):
					string1=population[0]
					string2=population[1]
					new_string=[]
					for l in range(5):
						stringt=crossover(string1[l],string2[l],length)
						new_string.append(stringt)
						new_gen.append(new_string)
				population1=population
				population=new_gen
				generation += 1
			value=[]
			for a in range(5):
				value.append(bintoflo(population1[0][a]))
			print "For population size",population_size,"and iteration ",iter_value
			print value
			plt.plot(range(iter_value),plot,c='r')
			plt.title("Genetic Algorithm")
			plt.show()
																											
ga()

