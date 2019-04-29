#--------------------------LOGIC---------------
# 
#
#
#

import copy
import numpy as np
target = "amitlovesgeneticalgorithm"
population = []
poolsize = 10
numPeople = 4

def s(str1, str2):
	a = 0
	for i in range(len(str1)):
		a+=((ord(str1[i]) - ord(str2[i])) **2)
	
	return np.sqrt(a)
	
def foundGoal():
	for i in range(len(population)):
		if((population[i] == target)):
			return i
	return -1
	
def getRandomString(target):
	s = ""
	for i in range(len(target)):
		num = np.random.randint(ord('a'), ord('z'))
		s+= chr(num)
	
	return s
	
def initializePopulation():
	for i in range(numPeople):	population.append(getRandomString(target))
	
	
def mutation(str1):
	r_ind = np.random.randint(len(str1))
	r_char = chr(np.random.randint(ord('a'), ord('z')))
	
	sList = list(str1)
	sList[r_ind] = r_char
	return ''.join(sList)
	
#Takes two string and returns fittest one
def selection(stringList):
	minIndex = -1
	minDist = 100000000
	for i in range(len(stringList)):
		currDist = s(stringList[i], target)
		if(currDist < minDist):
			minDist = currDist
			minIndex = i
			
	return stringList[minIndex]
	
def doCrossOver():
	return np.random.rand() > 0.5
	
def doMutation():
	return np.random.rand() > 0.5

#One point Crossover	
def crossOver(str1, str2):
	ind = np.random.randint(len(str1))
	offSpring1 = str1[:ind] + str2[ind:]
	offSpring2 = str2[:ind] + str1[ind:]
	
	return offSpring1, offSpring2
	
def v(s1, s2):
	if(doCrossOver()): s1, s2 = crossOver(s1, s2)
	offSpringList1 = []
	offSpringList2 = []
	
	for i in range(poolsize):
		#Pool1
		if(doMutation()):
			offSpringList1.append(mutation(s1))
		else: 
			offSpringList1.append(s1)
		
		#Pool2
		if(doMutation()):
			offSpringList2.append(mutation(s2))
		else: 
			offSpringList2.append(s2)
			
		#Selection
	return selection(offSpringList1), selection(offSpringList2)
		
def geneticAlgorithm():
	initializePopulation()
	iter = 0
	while(foundGoal() == -1 and iter < 1e8):
		parent1, parent2 = np.random.randint(0, numPeople, size = (2))
		print(population[parent1], population[parent2])
		population[parent1], population[parent2] = v(population[parent1], population[parent2])
		iter+=1
		
	print("Found Goal in iteration = " , iter, "Goal = ", population[foundGoal()])
	

##CHECK
geneticAlgorithm()