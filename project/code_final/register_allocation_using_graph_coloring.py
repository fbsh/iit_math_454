import imp
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import numpy as np
import random

VARS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "u", "v", "w", "x", "y", "z"]
COLORS = ["red", "green", "blue", "black", "yellow", "purple", "gray"]

def construct_graph_from_instructions(instructions):

    def parse_inst(inst):
        items = inst.split()
        _assign = items.index(":=")
        dests = [v for v in items[:_assign] if v in VARS]
        srcs = [v for v in items[_assign+1:] if v in VARS]
        return dests, srcs

    parsed_insts = [parse_inst(i) for i in instructions]

    V = list(set([j for i in parsed_insts for j in i[0]+i[1]]))

    E = [ e
         for S, T in parsed_insts for e in list(itertools.product(S, T))
    ]

    G = nx.Graph()
    G.add_nodes_from(V)
    G.add_edges_from(E)

    return G

def plot_graph(G, color_map=None, title=None):
    # print(color_map)
    plt.figure()  
    plt.title(title)
    nx.draw(G, pos=nx.circular_layout(G), with_labels=True, font_weight='bold', node_color=color_map)
    plt.show()


def graph_color_done(M, color_solution):
    N = len(M)
    for i in range(N):
        for j in range(i+1, N):
            if M[i][j]:
                if color_solution[j] == color_solution[i]:
                    return False
    return True


def graph_color_recursive(M, N_color_used, color_solution, d):
   
    if d == len(M):
        if graph_color_done(M, color_solution):
            return color_solution
        return None
    
    for j in range(1, N_color_used+1):
        # print(color_solution, d)
        color_solution[d] = j
        if graph_color_recursive(M, N_color_used, color_solution, d+1):
            return color_solution
        color_solution[d] = 0

    return None


def graph_coloring(G, N_color_used):
    M = nx.adjacency_matrix(G).todense()
    M = np.squeeze(np.asarray(M))
    color_solution_init = [0 for _ in M]
    color_solution = graph_color_recursive(M, N_color_used, color_solution_init, 0)
    return color_solution


def spilling_graph(G):
    degrees = {node:val for (node, val) in G.degree()}
    degrees_e = {(i,j): degrees[i]+degrees[j] for i,j in G.edges}
    e_removed = max(degrees_e, key=degrees_e.get)

    def select_new_node(G):
        while True:
            new_node = random.sample(VARS, 1)[0]
            if new_node in G.nodes:
                continue
            else:
                return new_node

    new_node = select_new_node(G)
    G.remove_edge(*e_removed)
    G.add_node(new_node)
    G.add_edge(e_removed[0], new_node)
    G.add_edge(e_removed[1], new_node)

    return G
