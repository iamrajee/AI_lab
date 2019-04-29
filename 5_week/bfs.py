#========================================Name==============================================#
#@Rajendra Singh

#=====================================Imports================================================#
from __future__ import print_function
import numpy as np
import copy
from Queue import Queue

#=====================================mat_class================================================#
class mat_class(object):
	def __init__(self, M):
		self.M = M

	def __eq__(self, other):
		n = other.M.shape[0]
		for i in range(n):
			for j in range(n):
				if other.M[i, j] != self.M[i, j]:
					return False
		return True

	def __hash__(self):
		return hash(str(self.M))
#=====================================person_class class================================================#
class person_class(object):
    def __init__(self, name, age):
        self.name, self.age = name, age

action = ["left", "right", "up", "down"]

#=====================================Callng================================================#
q = Queue()
obj = person_class("rajendra", 21)
q.put(obj)
temp = q.get()
print(temp.name, temp.age)