# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 13:53:25 2023

@author: cartin
"""

def connectList(e_path, node):
    """
    Given an e_path through the graph, which may be comprised of multiple
    components, and the PD code for a particular node in the graph, find two
    lists of tuples.
    
    The first list seg_list is in the format (seg, index) for
    each dart incident to the node, where seg is the index of the component
    segment in e_path, and index is where the dart is in the list for that
    segment.
    
    The second list connect_list gives a list of tuples giving the connections
    between the darts for the node. For example, the list [(d0, d1), (d3, d2)]
    indicates the connections d0 -> d1, d3 -> d2 for the Eulerian circuit
    through the node with PD code [d0, d1, d2, d3].
    """
    
    # Definitions
    
    dart_index_list = [0, 1, 2, 3]
    seg_list = [(-1, -1) for iii in range(4)]
    connect_list = []
    
    # Search for first dart in PD code, and see which dart is
    # its neighbor in the same component of the circuit
    
    no_first_dart = True
    e_path_sublist_index = 0
    
    while no_first_dart:
        if node[0] in e_path[e_path_sublist_index]:
            sub_path = e_path[e_path_sublist_index]
            len_sub_path = len(sub_path)
            first_dart_index = sub_path.index(node[0])
            
            # Other dart follows first dart in sub_path
            
            if sub_path[(first_dart_index + 1) % len_sub_path] in node:
                other_dart = sub_path[(first_dart_index + 1) % len_sub_path]
                other_dart_index = node.index(other_dart)
                
                seg_list[0] = (e_path_sublist_index, first_dart_index)
                seg_list[other_dart_index] = (e_path_sublist_index, (first_dart_index + 1) % len_sub_path)
                
                connect_list += [(node[0], other_dart)]
                
            # Other dart precedes first dart in sub_path
            
            elif sub_path[(first_dart_index - 1) % len_sub_path] in node:
                other_dart = sub_path[(first_dart_index - 1) % len_sub_path]
                other_dart_index = node.index(other_dart)
                
                seg_list[0] = (e_path_sublist_index, first_dart_index)
                seg_list[other_dart_index] = (e_path_sublist_index, (first_dart_index - 1) % len_sub_path)
                
                connect_list += [(other_dart, node[0])]
                
            no_first_dart = False
            
            # Remove indices from dart_index_list
            
            dart_index_list.remove(0)
            dart_index_list.remove(node.index(other_dart))
            
        else:
            e_path_sublist_index += 1

    # Find ordering of remaining two darts in PD code
    
    other_dart = node[dart_index_list[0]]
    other_dart_index = node.index(other_dart)
    
    final_dart = node[dart_index_list[1]]
    
    no_other_dart = True
    e_path_sublist_index = 0
    
    while no_other_dart:
        if other_dart in e_path[e_path_sublist_index]:
            sub_path = e_path[e_path_sublist_index]
            len_sub_path = len(sub_path)
            other_dart_index = sub_path.index(other_dart)
            
            # Last dart follows other dart in sub_path
            
            if sub_path[(other_dart_index + 1) % len_sub_path] == final_dart:
                
                seg_list[dart_index_list[0]] = (e_path_sublist_index, other_dart_index)
                seg_list[dart_index_list[1]] = (e_path_sublist_index, (other_dart_index + 1) % len_sub_path)
                
                connect_list += [(other_dart, final_dart)]
                
            elif sub_path[(other_dart_index - 1) % len_sub_path] == final_dart:
                
                seg_list[dart_index_list[0]] = (e_path_sublist_index, other_dart_index)
                seg_list[dart_index_list[1]] = (e_path_sublist_index, (other_dart_index - 1) % len_sub_path)
                
                connect_list += [(final_dart, other_dart)]
                
            no_other_dart = False
        
        else:
            e_path_sublist_index += 1
            
    # Return results
    
    return [seg_list, connect_list]