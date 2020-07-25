# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 08:12:51 2019

@author: cartin
"""

from functools import reduce
from Graphmaker import createSequences, modOrbit

###############################################################################

def permMaker(seq_length, max_num, curr_seq_list = []):
    """
    A list of lists is constructed recursively, where each list
    has seq_length elements, each of which is in range(max_num),
    and the elements satisfy iii_1 < iii_2 < ... iii_{max_num}.
    """
    
    if curr_seq_list == []:
        return permMaker(seq_length, max_num, [[iii] for iii in range(max_num)])
    elif len(curr_seq_list[0]) == seq_length:
        return curr_seq_list
    else:
        new_curr_seq_list = []
        for sequence in curr_seq_list:
            if sequence[-1] + 1 < max_num:
                new_curr_seq_list += permMaker(seq_length, max_num, [sequence + [iii] for iii in range(sequence[-1] + 1, max_num)])

        return new_curr_seq_list
    
###############################################################################

Nmin = 3                            # Minimum, maximum number of nodes for graphs
Nmax = 4

resultDict = {}

for N in range(Nmin, Nmax + 1):     # Number of nodes (vertices + crossings) in graph
    
    # Define final list of graphs for each number of nodes
    
    finalGraphList = []
    finalGraphDict = {iii : [] for iii in range(1, N + 1)}
    
    # Create all possible lists of length N lists with entries of +/- 1 (for
    # a crossing) or +/- 2 (for a vertex)
    
    signList = []
    
    for iii in range(4 ** N):
        tempList = [0 for jjj in range(N)]
        kkk = 0
        
        while kkk < N:
            if iii % 4 == 0:
                tempList[kkk] = -2      # Vertex, upper edge on odd label
            elif iii % 4 == 1:
                tempList[kkk] = -1      # Crossing, upper edge on odd label
            elif iii % 4 == 2:
                tempList[kkk] = 1       # Crossing, upper edge on even label
            else:
                tempList[kkk] = 2       # Vertex, upper edge on even label
                
            iii = iii // 4
            kkk += 1
            
        # If tempList includes two crossings that can be removed by a RII
        # move, then do not include tempList; do not have to worry about RI
        # moves, since these would not occur in a prime graph hot off the press
        
        flag = False
        
        for jjj in range(N):
            if tempList[jjj] * tempList[(jjj + 1) % N] == -1:
                flag = True
                break
            
        # If tempList is all crossings, do not include in signList
            
        if abs(reduce((lambda x, y: x * y), tempList)) != 1:
            signList += [tempList]
            
    # Create sequences of length N, and then for each such sequence, add
    # crossing/vertex information to each node, and see if each of these new
    # sequences are isomorphic to previous results; if not, include in
    # finalGraphList.

    processList = createSequences(N)
    
    for graph in processList:
        print(graph)
        
    print('---')
    
    for nextGraph in processList:
        
        # Go through all possible node types from signList, add to nextGraph,
        # and see if this graph is isomorphic to a previous graph
        
        for signChoice in signList:
            
            # Check to see if RII move can be used to remove this choice from
            # the queue; unnecessary to check RI moves, since these would not
            # appear in a prime graph sequence. Here are the sub-sequences to
            # check for, with c = +/- 1:
            #
            #   (i, j, c)(j + 1, i + 1, -c)     case (1)
            #   (i, j, c)(j + 1, i - 1, -c)     case (2)
            #   (i, j, c)(j - 1, i - 1, -c)     case (3)
            #   (i, j, c)(j - 1, i + 1, -c)     case (4)
            
            tempGraph = [nextGraph[iii] + [signChoice[iii]] for iii in range(N)]
            
            flag = False
            
            for nodeIndex in range(N):
                iii, jjj = tempGraph[nodeIndex][0], tempGraph[nodeIndex][1]
                
                # Cases (1) and (2)
                
                jjjIndex = ((jjj + 1) % (2 * N)) // 2
                
                if abs(tempGraph[jjjIndex][1] - iii) == 1 and tempGraph[nodeIndex][2] * tempGraph[jjjIndex][2] == -1:
                    flag = True
                    # keepIndex = nodeIndex
                
                # Cases (3) and (4)
                
                jjjIndex = ((jjj - 1) % (2 * N)) // 2
                
                if abs(tempGraph[jjjIndex][1] - iii) == 1 and tempGraph[nodeIndex][2] * tempGraph[jjjIndex][2] == -1:
                    flag = True
                    # keepIndex = nodeIndex
            
            if flag:
                # print('Node index', keepIndex, '; rejected:', tempGraph)
                continue
            
            # If RII test passed, go through all isomorphic sequences, find
            # lowest order sequence, and see if it has already been obtained
            
            tempGraph = modOrbit(tempGraph, 2 * N, crossing = True)
            
            if tempGraph not in finalGraphList:
                finalGraphList += [tempGraph]
            
            # print('graph:', tempGraph)
            
    print('Total num of graphs obtained =', len(finalGraphList))
    
    # Process graphs for number of vertices; place graphs into finalGraphDict
    # with key as vertex number
    
    for graph in finalGraphList:
        numVert = 0
        
        for label in graph:
            if abs(label[2]) == 2:
                numVert += 1
                
        finalGraphDict[numVert] += [graph]
        
    # Print graphs by vertex number
    
    for vertClass in range(N):
        print('Num of vertices =', vertClass + 1, '; num of graphs = ', len(finalGraphDict[vertClass + 1]))
        for graph in finalGraphDict[vertClass + 1]:
            print(graph)
        print('---')
    
    print('===')