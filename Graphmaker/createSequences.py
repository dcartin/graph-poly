# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 09:16:20 2019

@author: cartin
"""

from Graphmaker.addPair import addPair
from Graphmaker.isRealizable import isRealizable
from Graphmaker.modOrbit import modOrbit
from Graphmaker.notComposite import notComposite

def createSequences(num_nodes, crossing = False):
    """
    Given a number of nodes num_nodes, this procedure creates all realizable
    non-isomorphic sequences of that length. The sequences are then returned.
    """
    
    # Find sequences with (even, odd) pairs and no pair having numbers
    # differing by one
    
    print('Number of nodes N =', num_nodes)
    
    result = addPair(0, [(2 * iii + 1) for iii in range(num_nodes)], 2 * num_nodes)
    result.sort()
    print('Total number of sequences =', len(result))
    
    # Remove any other sequences isomorphic to other sequences by
    # adding a constant mod num_nodes
    
    nextQueue = []
    
    while len(result) > 0:
        nextSequence = result.pop(0)
        # flag = False
    
        isoSequence = modOrbit(nextSequence, 2 * num_nodes)
        # isoSequenceList = modOrbit(nextSequence, 2 * num_nodes, full_list = True)
    
        # for isoSequence in isoSequenceList:
        #     if isoSequence in nextQueue:
        #         flag = True
        #         break
    
        # [isoSequence, bbb] = modOrbit(nextSequence, 2 * num_nodes)
        
        if isoSequence not in nextQueue:
            nextQueue += [nextSequence]
    
        # if not flag:
        #     nextQueue += [nextSequence]
    
    print('Number of non-isomorphic sequences =', len(nextQueue))
    
    # Go through results and see which sequences are *not* composite
    
    finalList = []
    
    for sequence in nextQueue:
        if notComposite(sequence) and isRealizable(sequence):
            finalList += [sequence]
    
    print('Number of realizable non-composite sequences =', len(finalList))
    
    # If crossing is True, add vertex information to end of each label pair, so
    # that graphs reported out are all vertices; otherwise, just node labels
    
    if crossing:
        return [[[pair[0], pair[1], 0] for pair in graph] for graph in finalList]
    else:
        return finalList