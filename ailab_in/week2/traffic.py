#Team - Rajendra singh(111601017), Surendra baskey(111601027), Sachin hansda(111601019)#






#-------------------------------------Imports--------------------------------------------------------#
import pickle
import numpy as np
import pandas as pd
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

#--------------------------------------------Read data-----------------------------------------------#
path1 = "/home/rajendra/ailab/week2/roads/road"
m = pickle.load(open(path1,"rb"))
# print(m, type(m), np.shape(m), m[0,1])

path2 = "/home/rajendra/ailab/week2/roads/vehicle"
p = pickle.load(open(path2,"rb"))
# print(p, type(p), np.shape(p), p[0,1])

path3 = "/home/rajendra/ailab/week2/roads/time"
t = pickle.load(open(path3,"rb"))
# print(t, type(t), np.shape(t))

#--------------------------------------Class for vehicle--------------------------------------------#
class car:
    def __init__(self,tx,i, pi):
        self.tx = tx
        self.i = i
        self.pi = pi
    def __cmp__(self, other):#comparing two class of this type is equivalent to comparing this return value  
        return cmp(self.tx, other.tx) 

#-------------------------------Initialisation and declaration----------------------------------#
q = Q.PriorityQueue()#queue initialised
w, h = 10, 10

r = [[0 for x in range(w)] for y in range(h)] #matrix for keeping track of no. of vehicle on road
w, h = 5, 100

result = [[0 for x in range(w)] for y in range(h)] #matrix for storing result

for i in range(0,100):#puting the car in queue for first time
    q.put(car(t[i][0,0],i, 0))
    result[i][0] = t[i][0,0]

#-------------------------------------------Loop till queue not empty--------------------------------#
while not q.empty():
    v = q.get()
    if v.pi != 0: #reduce no. of vehicle on previous road
        s_prev = p[v.i,v.pi-1] #source during previos transition
        d_prev = p[v.i,v.pi]     #dest during previos transition
        r[s_prev][d_prev] -= 1
    if v.pi < 4: 
        s = p[v.i,v.pi]
        d = p[v.i,v.pi+1]
        x = r[s][d] #no. of vehicle on current vious road
        
        speed = np.exp(0.5*x)/(1 + np.exp(0.5*x)) + 15/(1 + np.exp(0.5*x))
        dist = m[s,d]
        delta_t = dist/speed
        v.tx+=delta_t#updste time
        v.pi+=1#increse path index
        result[v.i][v.pi] = v.tx
        r[s][d]+=1          #increase no. of vehicle on coming road
        q.put(v)    #insert vehicle in queue again


#--------------------------------------------Result---------------------------------------------------#
for ele in result:
    print(ele)
result = pd.DataFrame(result)
result.to_csv("result.csv")