# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 11:57:12 2020

@author: cartin
"""

def planarDiagram(seq, f_list):
    """
    Given DT sequence and orientation lists for a graph,
    return the planar diagram list for that sequence, and
    the type list for each node.
    """
    
    # Find number of nodes
    
    num_node = len(seq)
    
    # Create PD list and node type lists to return
    
    pd_list = [[] for iii in range(num_node)]
    type_list = [0 for iii in range(num_node)]
    
    # Go through the DT sequence, and find the PD sequence;
    # at first, we tack the type list onto the end of the PD
    # sequence, so we can sort the sequence, then strip off
    # the type information at the end.
    
    for jjj in range(num_node):
        node = seq[jjj]
        
        # Check that node is of form [even, odd]
        
        if node[0] % 2 != 0 or node[1] % 2 != 1:
            print('Incorrect form for node', jjj)
            return []
        
        # If node[2] is negative, this means the even label is
        # the undercrossing or the lower edge, if a vertex
        
        if node[2] < 0:
            
            # Lower edge, f(i) = +1
            
            if f_list[node[0]] == 1:
                pd_list[jjj] = [node[0], node[1], (node[0] + 1) % (2 * num_node),
                                (node[1] + 1) % (2 * num_node), -node[2]]
                
            # Lower edge, f(i) = -1
                
            elif f_list[node[0]] == -1:
                pd_list[jjj] = [node[0], (node[1] + 1) % (2 * num_node),
                                (node[0] + 1) % (2 * num_node), node[1], node[2]]
        
        # If node[2] is positive, this means the even label is
        # the overcrossing or the upper edge, if a vertex
        
        elif node[2] > 0:
            
            # Upper edge, f(i) = +1
            
            if f_list[node[0]] == 1:
                pd_list[jjj] = [node[1], (node[0] + 1) % (2 * num_node),
                                (node[1] + 1) % (2 * num_node), node[0], -node[2]]
                
            # Upper edge, f(i) = -1
            
            elif f_list[node[0]] == -1:
                pd_list[jjj] = [node[1], node[0], (node[1] + 1) % (2 * num_node),
                                (node[0] + 1) % (2 * num_node), node[2]]
                
        #print(node, f_list[node[0]], '>>>', pd_list[jjj])
                
    # Sort resulting PD list, then strip off
    # type information for separate list; since
    # SageMath wants the edge labels to start
    # with 1 vice 0, we add one here, to get
    # the range (1, ..., num_node) instead of
    # (0, ..., num_node - 1)
    
    pd_list.sort()
    
    type_list = [node[4] for node in pd_list]
    pd_list = [[node[iii] + 1 for iii in range(4)] for node in pd_list]
    
    # Return results
                
    return [pd_list, type_list]