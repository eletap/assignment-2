import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("fragments_file", help="name of input fragments file")

args = parser.parse_args()
f = open(args.fragments_file)

#Create directed graph-adjacency lists with dictionary.
graph={}
for line in f:
    l = line.rstrip()
    k=len(l)
    key=l[:k-1]
    value=l[1:]
    if key not in graph:
        graph[key] = []
    if value not in graph[key]:
        graph[key].append(value)
f.close()

#Method that implements the first part of the Hierholzer Algorithm.
#Use a random node (v) as a starting point. Move from node to node using edges we haven't used/visited yet. Repeat until we reach the original node(v).
def HierholzerAl(v, graph, oldpath):
    newpath=[]
    vstart=v
    newpath.append(v)
    while True:
        for n in graph[v]:
            if (edgeInPath(oldpath, v, n)==False) and (edgeInPath(newpath, v, n)==False):
                v=n
                newpath.append(v)
                break
        if vstart==v:
            break

    return newpath

#Method to check if we have already used a certain edge.
#e.g. if we want to see if the edge CGA is used then we have to check if GA comes right after CG in the path.
#Return True only when the above statement is correct. Otherwise (e.g. if the path is empty) return False.
def edgeInPath(path, v, n):
    f=False
    if path:
        for i in range(len(path)-1):
            if path[i]==v:
                if path[i+1]==n:
                    f=True
                    break
    return  f


#Call the HierholzerAl method to find the first eulerian path. If there is a node (u) which exists in the path but is connected to edges that are not in the path:
#repeat the HierholzerAl method with (u) as the starting node. Finally combine the paths that were found. Repeat until every edge is in the path.
v=random.choice(list(graph.keys()))
firstpath=[]
eulerian_path=HierholzerAl(v, graph, firstpath)
f=True
while f==True:
    f=False
    for i, u in enumerate(eulerian_path):
        for n in graph[u]:
            if edgeInPath(eulerian_path, u, n)==False:
                f=True
                newpath=eulerian_path[:i]+HierholzerAl(u, graph, eulerian_path)+eulerian_path[i+1:]
                eulerian_path=newpath
                break
        if f==True:
            break

#Create the final DNA output-string by using the first part of each node in the path (the common base of the fragments).
DNA=""
for p in eulerian_path[1:]:
    DNA+=p[0]
print(DNA)
