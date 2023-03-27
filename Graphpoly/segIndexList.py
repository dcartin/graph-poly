# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 13:52:36 2023

@author: cartin
"""

def segIndexList(e_path, node):
    """
    Given an e_path possibly composed of several different components, and the
    PD code for a node in the graph, find a list of tuples (seg, index), where
    for each dart in the PD code, seg is which segment the dart is in, and
    index is its location within the list for that segment.
    """
    
    seg_list = []
    
    for dart in node:
        
        no_dart = True
        e_path_sublist_index = 0
        
        while no_dart:
            if dart in e_path[e_path_sublist_index]:
                seg_list += [(e_path_sublist_index, e_path[e_path_sublist_index].index(dart))]
                no_dart = False
                
            else:
                e_path_sublist_index += 1
                
    return seg_list