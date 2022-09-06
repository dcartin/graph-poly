# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 13:34:17 2022

@author: cartin

This program takes an Eulerian circuit through a knotted 4-valent graph, and
returns the PD code for the knot diagram induced by this circuit.

When the induced knot diagram is created, there will often be times when two
or more edges are combined together into one. This is when the Eulerian circuit
does not change a vertex into an equivalent crossing, but instead "takes a
turn". Thus, we need a union-find data structure to keep track of which edges
should be grouped together in the final PD code for the induced knot diagram.
"""

#=============================================================================#

class UnionFind:
    
    def __init__(self, num_entries):
        self.num_entries = num_entries
        self.root_list = [iii for iii in range(num_entries)]
        
    #-------------------------------------------------------------------------#

    def rootList(self):
        return self.root_list
        
    #-------------------------------------------------------------------------#

    def nonIsoList(self):
        
        self.non_iso_list = []

        for item in range(self.num_entries):
            if self.root_list[item] == item:
                self.non_iso_list += [item]

        return self.non_iso_list
        
    #-------------------------------------------------------------------------#
                          
    def findRoot(self, index):
        
        # If the value of the root list at index is equal to index
        # (index is the root of a multiple item cluster) or num_entries
        # (index is a single item cluster), return index as the root
        # of the given cluster
        
        if self.root_list[index] == index or self.root_list[index] == self.num_entries:
            return index

        # Recursive piece if node is pointing to another node
        
        self.root_list[index] = self.findRoot(self.root_list[index])
        return self.root_list[index]
        
    #-------------------------------------------------------------------------#

    def Union(self, aaa, bbb):
    
        # To ensure that the lowest node number becomes the
        # root of each tree in the union-find structure, we
        # enforce aaa < bbb
        
        if aaa > bbb:
            aaa, bbb = bbb, aaa

        root_aaa = self.findRoot(aaa)
        root_bbb = self.findRoot(bbb)

        if root_aaa == aaa and root_bbb == bbb:
    
            # Both aaa and bbb are the roots of clusters;
            # add bbb to cluster for aaa, since aaa < bbb
            
            self.root_list[bbb] = aaa
    
        elif root_aaa == aaa:
    
            # aaa is the root of a cluster, but bbb is not; add
            # aaa to cluster for root_bbb if root_bbb < aaa,
            # otherwise, add root_bbb to new cluster for aaa
    
            if root_bbb < aaa:
                self.root_list[aaa] = root_bbb
            else:
                self.root_list[root_bbb] = aaa
    
        elif root_bbb == bbb:
    
            # bbb ifins the root of a cluster, but aaa is not; add
            # bbb to cluster for root_aaa since
            # root_aaa <= aaa < bbb
    
            self.root_list[bbb] = root_aaa
    
        else:
    
            # Neither aaa, bbb are roots of clusters; make
            # sure both are in the same cluster with
            # lowest root value
    
            if root_aaa > root_bbb:
                self.root_list[root_aaa] = root_bbb
            else:
                self.root_list[root_bbb] = root_aaa
        
#=============================================================================#

def createInducedKnot(graph):
    
    # Get required information from graph class object
    
    num_node = graph.numNodes()     # Number of nodes in original graph
    PD_code = graph.listPDCode()        # Planar diagram code for graph
    circuit = graph.listEPath()         # Final Eulerian circuit through graph
    
    # Create union-find data structure for half-edges
    
    dartData = UnionFind(4 * num_node)
    
    # Create list to write PD code for induced knot diagram
    
    knotCode = []
    
    # Create f(i) function list, for keeping track of the direction of the
    # overcrossing, as it passes over the undercrossing
    
    f_list = []
    
    # From given PD code, make a dict, with half-edge labels as keys, and
    # node labels as values. All half-edges should be incident on a node, so
    # all will appear as keys in the dictionary.
    
    nodeDict = {dart : node for node in range(num_node) for dart in PD_code[node]}
    
    # for iii in range(num_node):
    #     for dart in PD_code[iii]:
    #         nodeDict[dart] = iii
            
    # From given PD code make a dict, with node labels as keys, and the PD
    # code for that node as value
    
    codeDict = {iii : PD_code[iii] for iii in range(num_node)}
            
    # Read through given PD code. If two darts have labels differing by one,
    # then either they make up the same edge, or else they are opposite sides
    # of a node. If not, then they pass through an node, making a turn at the
    # node, so the node must not be included in the final list.
    
    for iii in range(4 * num_node):
        current_dart = circuit[iii]
        next_dart = circuit[(iii + 1) % (4 * num_node)]
        
        if (abs(current_dart - next_dart) == 1 or                                 \
            abs(current_dart - next_dart) == (4 * num_node - 1)):
            
            if nodeDict[current_dart] != nodeDict[next_dart]:
                
                # Darts make up a single edge
                
                dartData.Union(current_dart, next_dart)
                
            elif nodeDict[current_dart] in codeDict.keys():
                
                # This is a node that has not been dealt with yet in circuit
                
                # Find common node of half-edges
                
                current_node = nodeDict[current_dart]
                
                # Half-edges are on opposite sides of a node. However, we must
                # ensure that the PD code is updated properly for any changes
                # due to turns (i.e. vertices removed from the graph). Turns
                # can change the ordering of a portion of the sequence, but
                # not a global change in orientation.
                
                [iii, jjj, kkk, lll] = PD_code[current_node]
                
                # We check to see if the ordering of half-edges in the list
                # circuit has changed the orientation of the edges at the
                # crossing. We first find the order of the undercrossing edge
                # by finding the indices of iii, kkk in circuit. We assume that
                # for this crossing, the half-edge labels on the same edge
                # differ by 1, so either the difference is \pm 1, or \pm (N - 1)
                # if the half-edge labels are at the extreme ends of the list
                # circuit.
                
                under_index = circuit.index(kkk) - circuit.index(iii)
                
                if under_index == 1 or under_index == -(4 * num_node - 1):
                    temp_PD_code = [iii, jjj, kkk, lll]
                elif under_index == -1 or under_index == (4 * num_node - 1):
                    temp_PD_code = [kkk, lll, iii, jjj]
                    
                knotCode += [temp_PD_code]
                
                # For overcrossing, see which way the sequence passes, and
                # update f(i) for crossing i accordingly. To do this, see what
                # sense the half-edge labels change in the crossing. Suppose
                # the crossing in the original graph is (i, j, i + 1, j + 1),
                # where the numbers refer to the *indices* of the half-edges
                # as given in the list circuit, i.e. their ordering in the path.
                # Then the overcrossing is right-to-left, and f(i) = +1. If the
                # order is reversed in the induced knot, with (i, j, i - 1, j - 1),
                # then the overcrossing is still right-to-left. Thus, for a
                # crossing (a, b, c, d), we need to look at the product
                # (c - a)(d - b), to see what the sense is of the induced knot
                # crossing versus the one in the original graph.
                
                dirProd = under_index * (circuit.index(lll) - circuit.index(jjj))
                
                if dirProd == 1 or dirProd == (1 - 4 * num_node):
                    f_list += [1]
                else:
                    f_list += [-1]
                
                # Combine half-edges on overcrossing
                
                dartData.Union(codeDict[current_node][1], codeDict[current_node][3])
                
                # To ensure that a node is not included twice, remove node
                # from codeDict
                
                del codeDict[current_node]
                
        else:
            
            # Two half-edges pass through node via a "turn", so combine them
            # in union-find data structure
            
            dartData.Union(current_dart, next_dart)
            
    # Using union-find data structure, switching from half-edges to edges, so
    # that each edge has its own distinct label
    
    for iii in range(4 * num_node):
        dartData.findRoot(iii)
    
    rootList = list(set(dartData.rootList()))
    rootList.sort()
    
    for iii in range(len(knotCode)):
        knotCode[iii] = [rootList.index(dartData.findRoot(knotCode[iii][jjj])) for jjj in range(4)]
                
    # Return results
    
    return [knotCode, f_list]
        
#=============================================================================#