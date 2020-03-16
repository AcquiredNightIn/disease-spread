import scale as scale
import random as rd
import networkx as nx
import matplotlib.pyplot as plt
import pickle 
import csv



def write_to_file(X,Y,Max):
    try:
        with open("ScaleInv{}.txt".format(Max), "a+") as outfile:
            data = "\n{},{}".format(X, Y)
            outfile.write(data)
    except IOError:
        print("error writing to file!")
    return


def random_att(G, num_nodes, num_edges,iterat,attrib,initial_val,iteration_global):
    current_nodes = list(G.nodes)
    #tot = G.number_of_nodes()
    for j in range(num_nodes):
        next_num = "RA" + str(j) + str(iterat) + str(iteration_global)
        G.add_node(next_num)
        G.nodes[next_num][attrib] = initial_val
        select = rd.sample(current_nodes, num_edges)
        numb = [next_num] * num_edges
        edge_set = zip(numb, select)
        G.add_edges_from(edge_set)
    return


def random_rem(G, num_nodes):
    if num_nodes == 0:
        return
    current_nodes = list(G.nodes)
    #print("nodestot",len(current_nodes))
    select = rd.sample(current_nodes, num_nodes)
    G.remove_nodes_from(select)
    return






def PA_growth(graph, num_nodes, num_edges, iterat,attrib,initial,iteration_global):
    if num_nodes == 0:
        return None
    for i in range(num_nodes):
        distribution = []
        extend = distribution.extend
        for each in graph.degree():
            #num = [each[0]]*each[1]
            extend([each[0]]*each[1])
        
        next_num = int(graph.number_of_nodes())*(iteration_global+1) + i 
        while next_num in set(graph.nodes()):
            next_num += 1
        graph.add_node(next_num)
        graph.nodes[next_num][attrib] = initial
        selected = rd.sample(distribution, num_edges)
        numb = [next_num] * num_edges
        edge_set = zip(numb, selected)
        graph.add_edges_from(edge_set)
    return
    
def target_removal(graph, num_nodes):
    if num_nodes == 0:
        return None
    ordered = sorted(graph.degree, key=lambda x: x[1], reverse=True)
    graph.remove_nodes_from(ordered[:num_nodes])
    #for i in range(0, num_nodes):
    #    target = ordered[i]
    #    graph.remove_node(target[0])
    return
    
def null_growth(graph=None, ssgrowth=None, edge_num=None, i=None,attrib=None,initial_val=None,iteration_global=None):
    return

def null_contraction(graph=None, sscontr=None, i=None):
    return

def dynamic_pop(graph, growth, contraction, ssgrowth, sscontr, steps, edge_num):
    for i in range(steps):
        contraction(graph, sscontr)
        growth(graph, ssgrowth, edge_num, i)
        #print("iteration\t", i)
    return



def dummy(starting,begin,maxim,step):
    for n in range(begin,maxim,step):
        seed = 1
        m = 5
        steps = 10
        ssg = int(n / steps)
        ssc = int(n / steps)
        
        test = scale.gen_BA(starting, m, seed)
        dynamic_pop(test, PA_growth, target_removal, 0, ssc, steps, m)
        deg, cnt = scale.distribution(test)
        gamma = scale.powerlaw_fit(deg, cnt)
        amount = float(n/starting)

        test.clear()
        print(amount, gamma)
        write_to_file(amount,gamma,maxim+starting)
    return 0



if __name__ == "__main__":
    dummy(10000,0,100,1)
    print("done")



