# #-------------------------------------Imports--------------------------------------------------------#
# import numpy as np
# import random
# from queue import Queue
# import copy
# import string
# import heapq

# #-------------------------------Initialisation and declaration----------------------------------#
# target = "rajendra loves genetic algorithm"
# l = len(target) #length
# pool = 50
# half_pool = int(pool/2)
# print("length =", len(target))
# p_cross = 0.7
# p_mutation = 0.8


# #------------------------------------------function for fitness, mutation, crossover, selection--------#
# def fitness(s): #s - temp string
#     sum_ = 0
#     for i in range(l):
#         # sum_ = sum_ + abs(ord(target[i])-ord(s[i]))
#         if target[i] == s[i]:
#             sum_+=1
#     return sum_

# def selection(s_sp,n): #ssp - statespace, n - no of element to select
#     fitness_list = []
#     for ele in s_sp:
#         fitness_list.append(fitness(ele))
#     selected = heapq.nlargest(n, fitness_list)
#     new_sp = []
#     for ele in selected:
#         new_sp.append(s_sp[fitness_list.index(ele)])
#     return new_sp

# def crossover(s1,s2):
#     idx = random.randint(0,l-1)
#     return s1[:idx]+s2[idx:],s2[:idx]+s1[idx:]
#     # m = random.randint(0,l-1)
#     # sample = random.sample(range(0,l), m)
#     # for i in range():

#     # # s1_ = None
#     # # for i in sample1:
#     # #     s1_+=s1[i]

# def mutation(s,n):
#     sample_ = random.sample(range(0,l), n)
#     mutated_pop = []  
#     for ele in sample_:
#         mutated_pop.append(s[:ele]+random.choice(string.ascii_lowercase + ' ')+s[ele+1:])
#     return mutated_pop

# def baised_toss(p):
#     if random.uniform(0,1) < p:
#         return 1
#     else:
#         return 0

# #------------------Initialise random parent-----

# state_space = []
# for i in range(pool):
#     state_space.append(None)


# def gen_algo(iter):
#     flag = 0
#     for i in range(iter):
#         if flag == 0:
#             s1 = ''.join(random.choice(string.ascii_lowercase + ' ') for _ in range(l))
#             s2 = ''.join(random.choice(string.ascii_lowercase + ' ') for _ in range(l))
#             flag = 1
#         else:
#             parent_sp = selection(state_space,2)
#             s1 = parent_sp[0]
#             s2 = parent_sp[1]
#             flag = 2
#         print("iter = ",i,"s1 = ", s1, "s2 = ", s2)
#         if(s1 == target or s2 == target):
#             print("target found")
#             break
    
#         if baised_toss(p_cross) == 1:
#             s1,s2 = crossover(s1,s2)
#         if baised_toss(p_mutation) == 1 or flag == 1:
#             pop1 = mutation(s1,half_pool)
#             pop2 = mutation(s2,half_pool)
        
#             #--------------updating state_space--------
#             for i in range(half_pool):
#                 state_space[i] = pop1[i]
#             for i in range(half_pool):
#                 state_space[half_pool+i] = pop2[i]


# #-----------------------------------Calling gentic algo --------------------#
# gen_algo(1000) 

import random,string
print(''.join(random.choice(str(1)+str(0)) for _ in range(10)),"{0:b}".format(37))

get_bin = lambda x, n: format(x, 'b').zfill(n)

print(get_bin(-1,5)[0])

# '{0:{fill}{width}b}'.format((x + 2**n) % 2**n, fill='0', width=n)