# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 09:19:09 2019

@author: cartin
"""

def isRealizable(DT_sequence, f_list = False):
    """
    Given a possible DT sequence of node labels, runs through DT algorithm
    to see if the sequence is realizable as a planar graph. If the sequence is
    non-realizable, the function returns False. If f_list is False, the
    function returns True for realizable sequences; if f_list is True, instead
    it returns the function f for orientations at all crossings.

    Parameters
    ----------
    DT_sequence : list
        List of either 2 or 3 element lists, representing the node labels for
        a graph, possibly with crossing or vertex type information.
    f_list : bool, optional
        Whether to return orientations. The default is False.

    Returns
    -------
    bool
        Is the sequence realizable?

    """
    
    # Find total number of labels (which is twice the number of nodes);
    # this will also act as the modulus in all cases.
    
    num_labels = 2 * len(DT_sequence)
    
    # Create a list which gives the values for a(iii)
    # for each node iii.
    
    A_value_list = [0 for iii in range(num_labels)]
    for pair in DT_sequence:
        A_value_list[pair[0]], A_value_list[pair[1]] = pair[1], pair[0]
    
    # Initialize queue A with first value iii as well as a(iii)
    
    A_queue = [min(DT_sequence[0][0], DT_sequence[0][1])]

    # Create list which gives values of function f(x);
    # since f(x) = {+1, -1}, we use f(x) = 0 for nodes
    # x where the value has not been set. The starting values
    # are given as f(0) = 1 and f(a(0)) = -1.
    
    f_value_list = [0 for iii in range(num_labels)]

    f_value_list[A_queue[0]] = 1
    f_value_list[A_value_list[A_queue[0]]] = -1

    # Initialize phi function; again, use 0 for undefined
    # values, since all should be +/- 1 when defined.
    
    phi_value_list = [[0 for iii in range(num_labels)] for jjj in range(num_labels)]

    # Start while loop for processing A queue
    
    while len(A_queue) > 0:
        
        # Get next node iii.
        
        next_node = min(A_queue)

        # Create interval [iii, a(iii)] mod the total number of nodes
        
        aaa_next_node = A_value_list[next_node]         # a(iii) for current iii
        yyy = (next_node + 1) % num_labels

        if next_node < aaa_next_node:
            next_node_loop = [iii for iii in range(next_node, aaa_next_node + 1)]
        else:
            next_node_loop = [iii for iii in range(num_labels) if iii not in range(aaa_next_node, next_node + 1)]

        # Set phi_iii(iii) = 1, and use this and next_node_loop to determine
        # the other phi_iii values
        
        phi_value_list[next_node][next_node] = 1
        
        while yyy != next_node:
            
            # Set phi_iii(xxx) based on whether a(xxx) is in part of loop
            # [iii, a(iii)] (taken mod the number of nodes)
            
            if A_value_list[yyy] in next_node_loop:
                phi_value_list[next_node][yyy] = - phi_value_list[next_node][(yyy - 1) % num_labels]
            else:
                phi_value_list[next_node][yyy] = phi_value_list[next_node][(yyy - 1) % num_labels]

            # Increment xxx mod number of nodes

            yyy = (yyy + 1) % num_labels

        # Create D queue, and run through its members to set f(x) or
        # reject the graph
        
        D_queue = [iii for iii in range(num_labels) if iii not in next_node_loop]
        
        while len(D_queue) > 0:
            
            # Select least member of D queue
            
            xxx = min(D_queue)
            
            # Go through a ton of if-then statements
            
            #-----------------------------------------------------------------#
            #-----------------------------------------------------------------#
            
            if xxx < next_node:                                 # x < i (i.e. next_node)
            
                if A_value_list[xxx] in next_node_loop:         # a(x) is in [i, a(i)]
                    
                    phi_product = phi_value_list[next_node][xxx] * phi_value_list[next_node][A_value_list[xxx]] * f_value_list[next_node]
                
                    if f_value_list[xxx] == 0:                  # f(x) is not defined
                    
                        f_value_list[xxx] = phi_product
                        f_value_list[A_value_list[xxx]] = -phi_product

                        # See if a(x - 1) != a(x) \pm 1 mod num_labels

                        if abs((A_value_list[(xxx - 1) % num_labels] - A_value_list[xxx]) % num_labels) != 1:
                            A_queue += [min(xxx, A_value_list[xxx])]
                            
                    else:                                       # f(x) is defined

                        if phi_product == - f_value_list[xxx]:
                            return False
            
                else:                                           # a(x) not in [i, a(i)]
                    
                    if phi_value_list[next_node][xxx] * phi_value_list[next_node][A_value_list[xxx]] == 1:
                        D_queue.remove(A_value_list[xxx])
                    elif phi_value_list[next_node][xxx] * phi_value_list[next_node][A_value_list[xxx]] == -1:
                        return False
                    else:
                        print('Another uh-oh')
                        
                D_queue.remove(xxx)                             # Do this regardless
                    
            #-----------------------------------------------------------------#
            #-----------------------------------------------------------------#
                        
            elif xxx > A_value_list[next_node]:                 # x > a(i) (i.e. a(next_node))
            
                if A_value_list[xxx] not in next_node_loop:     # a(x) not in [i, a(i)]
                
                    D_queue.remove(A_value_list[xxx])
                    
                else:                                           # a(x) in [i, a(i)]
                
                    if f_value_list[xxx] == 0:                  # f(x) is not defined
                    
                        f_value_list[xxx] = phi_value_list[next_node][xxx] * phi_value_list[next_node][A_value_list[xxx]] * f_value_list[next_node]
                        f_value_list[A_value_list[xxx]] = - f_value_list[xxx]

                        # See if a(x - 1) != a(x) \pm 1 mod num_labels

                        if abs((A_value_list[(xxx - 1) % num_labels] - A_value_list[xxx]) % num_labels) != 1:
                            A_queue += [min(xxx, A_value_list[xxx])]
                        
                D_queue.remove(xxx)                             # Do this regardless

            #-----------------------------------------------------------------#
            #-----------------------------------------------------------------#
            
        # D queue process is completed, with empty D queue, so remove i and a(iii)
        # (i.e. next_node and its A_value) from A
        
        A_queue.remove(next_node)
        
    # If the A queue has been processed and not already
    # returned a False value, then the graph is realizable
    # and return True (unless the orientation function f_list
    # is asked for, then return that)
    
    if not f_list:
        return True
    else:
        return f_value_list