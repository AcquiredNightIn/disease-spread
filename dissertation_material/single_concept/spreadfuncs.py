import networkx as nx 
import growth
import scale
import sim
import random as rd



def prob_gen(probability):
    return rd.random() < probability


def initalize_graph(graph, attrib, init_value):
    nodes_total = list(graph.nodes)
    for each_node in nodes_total:
        graph.nodes[each_node][attrib] = init_value
    return

def count_attrib_val(graph, attrib, value):
    nodes = list(graph.nodes(data=attrib))
    count = 0
    other = 0
    for each in nodes:
        if each[1] == value:
            count += 1
        else:
            other += 1
    return count


def add_infected_initial(graph, number, attribute, initial_value, final_value):
    nodes = list(graph.nodes)
    nodes = find_attributes(graph,nodes,attribute,initial_value)
    selected = rd.sample(nodes, number)
    for each_node in selected:
        graph.nodes[each_node][attribute] = final_value
    return


def find_attributes(graph, node_list, attr,value):
    value_list = []
    for each_node in node_list:
        if graph.nodes[each_node][attr] == value:
            value_list.append(each_node)
    return value_list


def spread_step(graph, attribute, spread_value, targetted_value, spread_prob=0.01):
    nodes = list(graph.nodes)
    spread_value_nodes = find_attributes(graph, nodes, attribute,spread_value)
    if len(spread_value_nodes) == len(nodes):
        return "All"
    elif len(spread_value_nodes) == 0:
        return "None"
    for each_value_node in spread_value_nodes:
        adjacent_nodes = graph.adj[each_value_node]
        target_adj_nodes = find_attributes(graph, adjacent_nodes, attribute,targetted_value)
        for each_target in target_adj_nodes:
            if prob_gen(spread_prob):
                graph.nodes[each_target][attribute] = spread_value
    return "Success_step"
    

def iterate_steps(iterations, graph, attribute, spread_value, targetted_value, spread_prob=0.01):
    for i in range(0,iterations):
        val = spread_step(graph,attribute,spread_value,targetted_value,spread_prob)
        if val != "Success_step":
            return val
    return "Complete_iter"

def random_change(graph, attribute, current_value, target_value, prob):
    nodes = graph.nodes()
    current_concept_list = find_attributes(graph,nodes,attribute,current_value)
    for each_current in current_concept_list:
        if prob_gen(prob):
            graph.nodes[each_current][attribute] = target_value


def run_sim(graph,edge_num,total_steps,spread_prob,recover_prob, growth_steps, attribute,initial_value, final_value, third_value,growth_factor,all_node_change,gm,cm):
    step_node_change = int(all_node_change/growth_steps)
    growth_number_steps = int(total_steps/growth_steps)
    spread_step(graph,attribute,final_value,initial_value,spread_prob)
    random_change(graph,attribute,final_value,third_value,recover_prob)
    for step in range(0,total_steps):
        if step % growth_number_steps == 0:
            print("step: ", step+1, "/ {}".format(total_steps), "add", step_node_change)
            sim.grow_network(graph,m,growth_factor,step_node_change,attribute,initial_value,step,gm,cm)
        spread_step(graph,attribute,final_value,initial_value,spread_prob)
        random_change(graph,attribute,final_value,third_value,recover_prob)
        num_nodes = nx.number_of_nodes(graph)
        num_initial = count_attrib_val(graph,attribute,initial_value)
        num_final = count_attrib_val(graph,attribute, final_value)
        prop_inf = round(num_final, 6)
        num_third = count_attrib_val(graph,attribute,third_value)
        print("step: ", step+1, "node_num: ", num_nodes, "prop: ", prop_inf, "num: ", num_third)
    
        
    print("initial: \t", num_initial)
    
    print("final: \t\t", num_final)

    print("third: \t\t", num_third)
    print("prop inf: \t\t", round(num_final/num_nodes, 6))
        











if __name__ == "__main__":
    initial_nodes = 1000
    m = 20
    test = scale.gen_BA(initial_nodes, m)
    spread_prob = 0.1
    recover_prob = 1.0
    attribute = 'concept'
    initial_value = 'sus'
    second_value = 'newly'
    third_value = 'complete'
    initalize_graph(test, attribute, initial_value)

    start_final = 100
    add_infected_initial(test, start_final, attribute, initial_value, second_value)
    #print(count_I)
    steps_total = 20
    gf = (1.0,0.0)
    gm = growth.PA_growth
    cm = growth.null_contraction
    growth_steps = int(steps_total/10)
    unit_node_change = int(1*initial_nodes/1)


    run_sim(test,m,steps_total,spread_prob,recover_prob,growth_steps,attribute,initial_value,second_value,third_value,gf,unit_node_change,gm,cm)


    #generate network
    #initialize concepts
    #number of 
    #change network top (or not) if step number == (verbosity)
        #growth
        #contraction
        #initialize new nodes
    #iterate step
        #first concept
        #second concept