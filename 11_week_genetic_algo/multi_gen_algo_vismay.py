from __future__ import print_function
import sys
import numpy as np
from random import randint
from random import choice
from copy import deepcopy

MAX_LEN = 64
POOLSIZE = 200
TOTAL_ITR = 500
THRESHOLD = -8

'''
----------------------------------------------------------------------
	IDEA OF IMPLEMENTATION:
	representation of the floating point number is done using the following idea
	> first generate a binary of length 64
	> this represents integers from 0 -> 2^64-1
	> this is the genetype of our programme
	> now the conversion of genotype to phenotype is done using the following idea
		> let genotype = b
		> find i =  int(b) .  this will span from 0 to 2^64-1
		> do mi =  i-(2^63) now we'll obtain a number between -2^63 and 2^63-1
		> do f = mi*2.04/(2^63) now we'll obtain a float between -2.04 and 2.04
		> we can reverse the following instructions to get back the genotype from the phenotype
	> crossover and mutaion are done using simple string manipulations (see code) 
----------------------------------------------------------------------
'''

'''integer to binary'''
def ib(x):
	return "{0:b}".format(x)

'''binary to integer'''
def bi(x):
	int(str(x),2)

'''to make the strings length equal to MAX_LEN'''
def beq(x):
	return x.zfill(MAX_LEN)

'''
	crossover of to string of ficed length
	mechanism self explanatory
'''
def crossover(s1,s2):
	a=""
	b=""
	for i in range(MAX_LEN):
		if randint(0,1):
			a+=s1[i]
			b+=s2[i]
		else:
			a+=s2[i]
			b+=s1[i]
	return a,b

'''
	mutating the string
'''
def mutate(string,ftscr=MAX_LEN):
	s = bytearray(deepcopy(string))
	k= len(s)
	total = randint(2,22)
	for j in range(total):
		i = randint(0,k-1)
		#i = np.clip((k-1) - int(k*np.random.normal()),0,k-1)
		if randint(0,1):
			s[i] = '0'
		else:
			s[i] = '1'
	return str(s)

'''
	return float value b/w (-2.04 to 2.04) from 
	a binary of length 64 (explained above)
'''
def retfloat(x):
	a = int(x,2)
	a-=(2**63)
	return (a*2.04)/(2**63)

def retInt(x):
	return int((x*(2**63))/2.04)+(2**63)

'''
	fitness function
'''
def fitness(x):
	s = 0.0
	for i in range(5):
		s += x[i]**2

	for i in range(5):
		s += int(x[i])

	for i in range(5):
		s += (x[i]**4) + np.random.normal()

	return s


if __name__=="__main__":
	
	a = beq(ib(randint(0,2**64-1)))
	b = beq(ib(randint(0,2**64-1)))

	c = retfloat(a)
	print(c)

	print(int(a,2),retInt(c))

	print(fitness([c]*5))

	a1 = [a]*5
	a2 = [b]*5

	itr = 0

	maxarr = []

	while itr<TOTAL_ITR:
		itr+=1

		a1n = []
		a2n = []

		
		#cross over
		# a1n and a2n are the crossover products
		for i in range(5):
			t1,t2 = crossover(a1[i],a2[i])
			a1n.append(t1)
			a2n.append(t2)

		pool = []
		fitpool = []
		for j in range(POOLSIZE):
			if randint(0,1):
				appending_one = [mutate(x) for x in a1n]
				appending_score = fitness([retfloat(x) for x in appending_one])
			else:
				appending_one = [mutate(x) for x in a2n]
				appending_score = fitness([retfloat(x) for x in appending_one])

			pool.append(appending_one)
			fitpool.append(appending_score)

		m1f = np.min(fitpool)
		m1farg = np.argmin(fitpool)
		m1 = pool[m1farg]

		pool.pop(m1farg)
		fitpool.pop(m1farg)

		m2f = np.min(fitpool)
		m2farg = np.argmin(fitpool)
		m2 = pool[m2farg]

		v1 = (  [   round(retfloat(x),4)   for x in m1])
		v2 = (  [   round(retfloat(x),4)   for x in m2])
		print(itr,v1,v2,end="")
		print(m1f,m2f)

		maxarr.append(min(m1f,m2f))

		if m1f<THRESHOLD or m2f<THRESHOLD:
			break

		a1,a2 = m1,m2
			

	print(retfloat(a),retfloat(b))

	np.savetxt('arr_out.txt',maxarr,delimiter=',')

	sys.exit(0)