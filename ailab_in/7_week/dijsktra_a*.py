import numpy as np
import copy

# A = [[1,3],[0,2,3],   [1,,4,5], [0,1,4,7],     [2,3,5,8],   [2,4,6,11],   [5,12], [3,13],   [4,9,14,15],[8,10],[9,11],[10,12],[6,11],[7,14],[13,15],[14,16],[11,15]]
# W = [[3,3],[3,10,2.5],[10,20,5],[3,,2.5,6,2.5],[20,6,15,10],[5,15,2.5,12],[2.5,1],[2.5,2.5],[10,6,6,4] ,[6,6], [6,4],[10,12],[6,11],[7,14],[13,15],[14,16],[11,15]]
Edgelist = [[0,1,3], [1,2,10], [0,3,10], [1,3,2.5], [2,4,20], [2,5,5], [3,4,6], [4,5,15], [5,6,2.5], [3,7,2.5], [4,8,10], [5,11,12], [6,12,1], [8,9,6], [9,10,6], [10,11,4], [11,12,11], [7,13,2.5], [8,14,6], [8,15,4], [11,16,2], [13,14,1], [15,16,10]]
print(len(Edgelist))

start = 13
goal = 6



templist = []
for i in range(0,len(Edgelist)):
    templist.append(Edgelist[i][0])
    templist.append(Edgelist[i][1])
n_ver = len(np.unique(templist))
print(n_ver)

Heu = []
adj_tuple = []
for i in range(0,n_ver):
    Heu.append([])
    adj_tuple.append([])
print(len(Heu), len(adj_tuple))

for i in range(0,len(Edgelist)):
    tempele1 = [Edgelist[i][1],Edgelist[i][2],0]
    adj_tuple[Edgelist[i][0]].append(tempele1)
    tempele2 = [Edgelist[i][0],Edgelist[i][2],0]
    adj_tuple[Edgelist[i][1]].append(tempele2)
    
print(len(adj_tuple))

for i,ele in enumerate(adj_tuple):
    print(i,ele)


def bfs(src,adj_tuple,goal):
    for ele in adj_tuple[src]:
        


# def A_start(E, H, start, goal):
#     for nb in E[start]:

# A_start(adj_tuple)
