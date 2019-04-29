#random search
import random
import math
import numpy as np
import matplotlib.pyplot as plt

iteration=[10,20,50,100,200,500]
for i in range(6):
	f=[]
	n=[]
	for k in range(5):
		n1=random.uniform(-2.04,2.04)
		n.append(n1)
	h1=0
	h2=0
	h3=0
	for l in range(5):
		h1=h1 + (n[l]*n[l])
		h2=h2 + math.floor(n[l])
		h3=h3 + ((l+1)*n[l]*n[l]*n[l]*n[l])
	h3 = h3 + np.random.normal(0,1)
	f.append([h1,h2,h3])
	optimal=n
	for j in range(1,iteration[i]):
		n=[]
		for k in range(5):
			n1=random.uniform(-2.04,2.04)
			n.append(n1)
		f1=0
		f2=0
		f3=0
		for l in range(5):
			f1=f1 + (n[l]*n[l])
			f2=f2 + math.floor(n[l])
			f3=f3 + ((l+1)*n[l]*n[l]*n[l]*n[l])
		f3 = f3 + np.random.normal(0,1)
		if(f1<=h1 and f2<=h2 and f3<=h3):
			if(f1<h1 or f2<h2 or f3<h3):
				h1=f1
				h2=f2
				h3=f3
				optimal=n
		f.append([f1,f2,f3])

	for k in range(5):
		n[k]=n[k]-(n[k]%0.01)
	print( "For",iteration[i],"iteration")
	print (n)
	print ("\n")
	plt.plot(range(iteration[i]),f,c='r')
	plt.ylabel=("function value")
	plt.xlabel=("iteration")
	plt.title("Random Search")
	plt.show()
	