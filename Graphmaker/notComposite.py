# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 09:19:14 2019

@author: cartin
"""

def notComposite(sequence):
    """
    Checks whether a given sequence of pairs of node labels is composite, i.e.
    there is a subsequence of values that is mapped to itself within the
    sequence.
    """

    # Find number of nodes from length of sequence (each pair in DT notation
    # represents a node)

    num_nodes = len(sequence)
    
    # First, we check whether there are any labels for a node which are both
    # odd or both even
    
    for iii in range(num_nodes):
        if (sequence[iii][0] - sequence[iii][1]) % 2 == 0:
            raise ValueError('The sequence has incorrect labels')

    # If the number of nodes is 1, or 2, all possible valid sequences are
    # composite. The sequence (0, 2)(1, 3) would already have given an error.

    if num_nodes <= 2:
        return False
    
    # From this point on, crossing information is not necessary, so filter out
    # this information (if present) and redefine sequence only in terms of its
    # raw DT labels.
    
    sequence = [[sequence[iii][0], sequence[iii][1]] for iii in range(num_nodes)]
    
    # For 3 nodes, the only valid sequence is (0, 3)(2, 5)(4, 1).
    
    if num_nodes == 3:
        if sequence == [[0, 3], [2, 5], [4, 1]]:
            return True
        else:
            return False
        
    # Now consider the case of four or more nodes, and check explicitly
    # whether there are sub-sequences of labels that are mapped to themselves,
    # corresponding to composite graphs. The process of constructing the
    # sequences already checks for two values that are mapped to themselves.
    # First, look at the case of odd num_nodes; here, we only need to look at
    # sub-sequences of 4, 6, ..., (num_nodes - 1) values, where there are 
    # 2 * num_nodes total values. This is because if e.g. four values are
    # mapped to themselves, so will the other (2 * num_nodes - 4). For even
    # num_nodes, we use the sub-sequences of 4, 6, ..., (num_nodes - 2), as
    # before (so num_values_list already captures these values), along with
    # *half* of those sub-sequences with num_nodes values. These are chosen to
    # be all sequences of num_nodes labels which do *not* include the label zero.
    # This is because if you have a case of one of the chosen sub_sequences,
    # the other half of the sequence will map to itself and include zero as a
    # label.

    # Go through the original sequence, and take the first 2, 4, ... label pairs
    # and see if (after sorting) these are the same as one of the sequences
    # in the test sequence list. If so, return False. Otherwise, return True
    # after all test sequences are tried.

    num_values_list = range(4, num_nodes, 2)

    for test_val in num_values_list:
        test_seq_list = [sorted([(nnn % (2 * num_nodes)) for nnn in range(iii, iii + test_val)]) for iii in range(2 * num_nodes)]
        
        for iii in range(num_nodes - (test_val // 2) + 1):
            if sorted([label for pair in sequence[iii : (iii + (test_val // 2))] for label in pair]) in test_seq_list:
                return False

    if num_nodes % 2 == 0:
        
        # Note the sequences are already sorted, so there is no reason to code this
        
        test_seq_list = [[(nnn % (2 * num_nodes)) for nnn in range(iii, iii + num_nodes)] for iii in range(1, num_nodes + 1)]

        for iii in range((num_nodes // 2) + 1):
            if sorted([label for pair in sequence[iii : (iii + (num_nodes // 2))] for label in pair]) in test_seq_list:
                return False
            
    # No sub-sequences mapped to themselves detected, so return True

    return True