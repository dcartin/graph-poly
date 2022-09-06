# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 07:52:36 2020

@author: cartin
"""

def labelReverse(pd_seq, min_label, max_label):
    """
    Given a list representing the PD notation for
    a knotted graph, made of edge labels which are
    integers from 1 to N, and two numbers min_label
    and max_label, reverse all integers in the PD
    notation whose index is between and including
    those for min_label and max_label. This requires
    that PD notation for affected nodes are permuted
    appropriately.
    """
    
    # Calculate number of edges
    
    num_edges = 2 * len(pd_seq)
    
    # Make list of labels to reverse
    
    num_rev_labels = (max_label - min_label + 1) % num_edges
    rev_label_list = [(min_label + iii - 1) % num_edges + 1 for iii in range(num_rev_labels)]
    
    # Reverse order of all numbers in
    # list rev_label_list
    
    new_seq = [[label if label not in rev_label_list else rev_label_list[(num_rev_labels - 1) - rev_label_list.index(label)] for label in node] for node in pd_seq]
    
    # For all nodes whose first label was reversed,
    # permute the edge labels so that the incoming
    # lower edge is in the correct spot after reversal
    
    new_seq = [node if node[0] not in rev_label_list else [node[2], node[3], node[0], node[1]] for node in new_seq]
    
    # Return results
        
    return new_seq