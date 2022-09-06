# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 09:21:04 2019

@author: cartin
"""

from Graphpoly.properPair import properPair

def addPair(next_even_num, missing_node_list, modulus):
    """
    Recursively find all permutations of missing_node_list where
    each pair of labels is separated by more than one mod the modulus.
    """

    num_missing_nodes = len(missing_node_list)

    # Make sure that next_even_num is really even

    if next_even_num % 2 == 1:
        return []

    # Base case: only one missing node is remaining, so check
    # whether they form a proper pair and add to the list

    if num_missing_nodes == 1 and properPair([next_even_num, missing_node_list[0]], modulus):
        return [[[next_even_num, missing_node_list[0]]]]

    # Continue recursion if more than one missing node to add; again
    # check that added pair is a proper pair, and use the next odd number
    # in the sequence.

    return sorted([[[next_even_num, missing_node_list[iii]]] + next_perm for iii in range(num_missing_nodes)
    for next_perm in addPair(next_even_num + 2, [nnn for nnn in missing_node_list if nnn != missing_node_list[iii]], modulus)
    if properPair([next_even_num, missing_node_list[iii]], modulus)])
