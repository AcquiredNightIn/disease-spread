import scale
import growth
import analysis
import copy
import networkx as nx
import numpy as np

def write_to_file(initial_size, node_change,regime,thresh):
    try:
        with open("deviation_{}_{}.txt".format(regime,thresh), "a+") as outfile:
            data = "\n{},{}".format(initial_size, node_change)
            outfile.write(data)
    except IOError:
        print("error writing to file!")
    return

def write_to_file3D(incr,decr, node_change,regime,thresh):
    try:
        with open("deviation_{}_{}.txt".format(regime,thresh), "a+") as outfile:
            data = "\n{},{},{}".format(incr,decr, node_change)
            outfile.write(data)
    except IOError:
        print("error writing to file!")
    return


def calc_data(current_graph, gamma_initial, normal_gamma_init):
    deg_cur, cnt_cur = scale.distribution(current_graph)
    gamma_cur = scale.powerlaw_fit(deg_cur, cnt_cur)
    normal_gamma_cur = gamma_cur - 2
    change = (gamma_initial - gamma_cur)/gamma_initial
    normal_change = (normal_gamma_init - normal_gamma_cur) / normal_gamma_init
    return change, normal_change




def grow_network(G, m, growth_factor, total_node_change,attrib,initial_val,iteration_global, growth_mech=growth.null_growth, contr_mech=growth.null_contraction):
    granularity = 10#int(num_nodes / 20)
    if growth_factor[0] == 0.0:
        growth_mech = growth.null_growth
    if growth_factor[1] == 0.0:
        contr_mech = growth.null_contraction
    ssg = abs(int((total_node_change * growth_factor[0]) / granularity))
    ssc = abs(int((total_node_change * growth_factor[1]) / granularity))
    #print("ssc",ssc)
    for step in range(0, granularity):
        print("growth step: ", step+1, "/",granularity)
        growth_mech(G,ssg,m,step,attrib,initial_val,iteration_global)
        contr_mech(G,ssc)


def additional_node_iterate(starting_nodes, edge_num, max_prop, num_incr_of_prop, grom, conm, growth_factor=(0,0), thresh=0.1):
    initial_graph = scale.gen_BA(starting_nodes, edge_num)
    deg_init, cnt_init = scale.distribution(initial_graph)
    gamma_init = scale.powerlaw_fit(deg_init, cnt_init)
    normal_gamma_init = gamma_init - 2
    diverge = False
    for incr in range(0, num_incr_of_prop+1):
        iter_graph = copy.deepcopy(initial_graph)
        if max_prop >= 1:
            total_node_change = int((max_prop * starting_nodes * incr)/ num_incr_of_prop)
        else:
            total_node_change = int(((1-max_prop) * starting_nodes * incr)/ num_incr_of_prop)

        grow_network(iter_graph,edge_num,growth_factor,total_node_change,grom,conm)
        change, normal_change = calc_data(iter_graph, gamma_init,normal_gamma_init)
        
        if normal_change > thresh:
            size_change = round(total_node_change/starting_nodes, 3)
            if growth_factor[0] < growth_factor[1]:
                size_change = - size_change
            
            write_to_file(growth_factor[0],size_change, str(grom.__name__ + conm.__name__),thresh)
            print(growth_factor[0],size_change, str(grom.__name__ + conm.__name__),thresh)
            iter_graph.clear()
            diverge = True
            break
        iter_graph.clear()
    if not diverge:
        write_to_file(growth_factor[0],max_prop, str(grom.__name__ + conm.__name__),thresh)
    initial_graph.clear()


def initial_node_iterate(start_nodes, final_nodes, num_steps, edge_num, max_prop, num_prop_increm, gm, cm, growth_factor):
    increment = int((final_nodes - start_nodes) / num_steps)
    for nodes in range(start_nodes, final_nodes, increment):
        #print("starting nodes: ",nodes)
        additional_node_iterate(nodes,edge_num,max_prop,num_prop_increm,gm,cm,growth_factor)


def iterate_growth_ratio(initial_nodes, edge_num, num_prop_increm, gm, cm, granularity=10):
    step_size = round(float(1.0 / granularity),2)
    for increase_num in np.arange(0.0,1.0+step_size, step_size):
        gf, max_prop = growth_factor(increase_num)
        additional_node_iterate(initial_nodes,edge_num,max_prop,num_prop_increm,gm,cm,gf)

def PA_proof(starting_nodes, edge_num, increase_prop, prop_steps):
    change_vals = []
    normal_change_vals = []
    for incr in np.linspace(0,increase_prop,prop_steps,endpoint=False):
        initial_graph = scale.gen_BA(starting_nodes, edge_num)
        deg_init, cnt_init = scale.distribution(initial_graph)
        gamma_init = scale.powerlaw_fit(deg_init, cnt_init)
        gf, max_prop = growth_factor(1.0)
        grom = growth.PA_growth
        conm = growth.null_contraction
        normal_gamma_init = gamma_init - 2



        iter_graph = copy.deepcopy(initial_graph)
        total_node_change = starting_nodes * incr

        grow_network(iter_graph,edge_num,gf,total_node_change,grom,conm)
        change, normal_change = calc_data(iter_graph, gamma_init,normal_gamma_init)
        incr = round(incr, 3)
        normal_change = round(normal_change, 3)
        change = round(change,3)
        write_to_file3D(incr,normal_change,change, str(grom.__name__ + conm.__name__),0)
        print(incr,normal_change,change, str(grom.__name__ + conm.__name__),0)
        normal_change_vals.append(normal_change)
        change_vals.append(change)
        iter_graph.clear()

        initial_graph.clear()
    
    return normal_change_vals, change_vals


def growth_factor(A):
    B = 1 - A
    A = round(A,3)
    B = round(B,3)
    gf = (A,B)
    if A - B < 0:
        max_prop = 0.001
    elif A - B >= 0:
        max_prop = 10
    return gf, max_prop



#def repeat_run(initial_num,final_num,iterations, repeats):
 #   for i in range(0,repeats):
  #      starting_nodes_iter(initial_num,final_num,iterations)
   # return



if __name__ == "__main__":
    
    m = 5
    n_0 = 10000
    n_end = 20
    max_prop = 20
    #start_it_steps = 50
    increm_prop = 100 #5
    

   
    norm_values, values = PA_proof(n_0,m,max_prop,increm_prop)
    avg = np.average(values)
    norm_avg = np.average(norm_values)
    print("\nAverage Change:", avg*100,"%")
    print("NormAverage Change:", norm_avg*100,"%")

    #    #iterate_growth_ratio(n_0, m, increm_prop,gm,cm,ratio_step_size)
    #    initial_node_iterate(n_0, n_end, start_it_steps, m, max_prop, increm_prop, gm, cm, growth_fac)

    #additional_node_iterate(n, m, max_prop, increm_prop, gm, cm, growth_fac)

#to do list

#iterate over initial node sizes, with basic growth mechanics, record max prop
#fix node size, itterate of growth factors, record max_prop