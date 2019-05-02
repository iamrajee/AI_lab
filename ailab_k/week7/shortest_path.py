import numpy as np 
from collections import deque

class Environment:
    def __init__(self , grid_info :list , distance_mat :np.ndarray):
        
        pass



def render_mat(mat:np.ndarray):
    if len(mat.shape) == 2:
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                print(mat[i,j], end="\t")
            print("\n", end="")

def read_heuristic_grid_file(fname="grid.txt"):
    grid_info = []
    with open(fname , "r") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
        for dat in lines:
            dat = dat.split()[:]
            node_num , hcoord = (eval(dat[0]) , eval(dat[1]))
            # print(node_num , hcoord)
            grid_info.append((node_num , hcoord))
    return grid_info

def read_network_file(fname="edge_list.txt"):
    adj_mat = None
    with open(fname , "r") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
        # print(lines)
        total_nodes = eval(lines.pop(0))
        # print("Total Nodes: {0}".format(total_nodes))
        adj_mat = np.zeros((total_nodes , total_nodes) , dtype=np.float)
        while len(lines) != 0:
            i , j , d = tuple([eval(dat) for dat in lines.pop(0).split()])
            adj_mat[i,j] = d
            adj_mat[j,i] = d
    return adj_mat


def main():
    grid_info = read_heuristic_grid_file()
    adj_mat = read_network_file()
    render_mat(adj_mat)

    pass 

if __name__ == "__main__":
    main()
    pass 
