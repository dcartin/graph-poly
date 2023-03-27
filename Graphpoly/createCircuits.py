# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 13:34:17 2022

@author: cartin

This program takes a description of a knotted 4-valent graph as a planar
diagram sequence, and finds all possible induced knot diagrams for the graph.
It uses Hierholzer's algorithm to do this.

The function is given two Python lists. The first list, PD_list, is the planar
diagram sequence for the graph. Every item in PD_list represents the half-edges
incident to a given node in the graph. This representation consists of a list
of four numbers, the labels of the four incident half-edges. The list assumes
an orientation on the graph, so it starts with the incoming half-edge that
passes under the crossing (or is equivalent to that for a vertex). The other
half-edges are then given in counter-clockwise order from the first half-edge.

NOTE: The labels of the half-edges are given in reference to a particular
oriented Eulerian circuit through the graph. In this orientation, half-edges
with even labels enter a node, while odd labels indicate half-edges leaving a
node.

The second list, type_list, gives the node state and information about how the
half-edges cross each other in the given orientation. A node state has
magnitude 1 if it is a crossing, and 2 if it is a vertex; the sign comes from
the value f(i) for the given node.
"""

from copy import deepcopy

#=============================================================================#

class Graph:
    def __init__(self, PD_code, type_list):
        
        if len(PD_code) != len(type_list):
            print('PD code has different length than type_list')
        self.num_node = len(PD_code)
        
        # Definitions
        
        self.cpath = []
        self.epath = []
        self.node_type_dict = {iii : type_list[iii] for iii in range(self.num_node)}
        self.PD_code = [[label for label in node] for node in PD_code]
        
        # Create a dictionary from PD code, with key as dart label, and value
        # as node the dart is incident to
        
        self.dart_dict = {iii : -1 for iii in range(4 * self.num_node)}
        
        for (node, dart_list) in enumerate(self.PD_code):
            for dart in dart_list:
                self.dart_dict[dart] = node
        
        # Create a dictionary from PD code, with key as node label, and
        # value as list of half-edges incident to the node.
        
        # This dict will be altered i løpet av programmet, to keep track of
        # which edges have been used. The original PD code will be used at the
        # end to find the PD code for the Eulerian circuit through the graph.

        self.dart_adj_dict = {iii : [dart for dart in self.PD_code[iii]]
                              for iii in range(self.num_node)}
        
        # Set starting dart, node
        
        self.current_node = 0
        self.current_dart = min(self.PD_code[0])
        
        # When the algorithm is executed, each edge is added to the path, then
        # the edge is removed. However, this means we need to keep trach of
        # what available edges can be traveled down next. Here we initialize
        # this list of next available edges. NOTE: we do *not* remove the
        # starting half-edge, since this would be done when the same edge is
        # used at the end of the path.
        
        # If the current node is a crossing, the edge opposite the current edge
        # is the only available edge for the next move; otherwise, all edges
        # except for the current edge are available.
        
        loc = self.dart_adj_dict[self.current_node].index(self.current_dart)
        
        if abs(self.node_type_dict[self.current_node]) == 1:
            self.next_dart_list = [self.dart_adj_dict[self.current_node][(loc + 2) % 4]]
        else:
            self.next_dart_list = [dart for dart in self.dart_adj_dict[self.current_node]
                                   if dart != self.current_dart]

    #-------------------------------------------------------------------------#
        
    def __eq__(self, other):
        """
        Check for equality between two graphs by testing their final Eulerian
        circuits. Since permuted versions of these circuits are considered
        equivalent, we use permutations for the equality test.
        """
        
        # Get other epath
        
        other_epath = other.listEPath()
        
        # Check lengths of epaths
        
        if len(self.epath) != len(other_epath):
            return False
        
        # Try all cyclic permutations of other.epath, and compare to
        # self.epath; include reversals of entire list
        
        for iii in range(len(self.epath)):
            new_epath = other_epath[iii:] + other_epath[:iii]
            if new_epath == self.epath:
                return True
            if new_epath.reverse() == self.epath:
                return True
            
        # No permutations work
        
        return False

    #-------------------------------------------------------------------------#
        
    def backtrack(self):
        """
        This goes back one step in the list cpath of half-edges, and moves the
        current node to the previous one in the temporary Eulerian circuit.
        """
        
        # The backtrack procedure is only used when the current node has no
        # available edges, so add current edge to epath (the final Eulerian
        # circuit). Pop twice to get both half-edges corresponding to given
        # edge
        
        dart = self.cpath[-2]
        
        self.epath += [self.cpath[-1], self.cpath[-2]]
        self.cpath = self.cpath[:-2]
        
        # Find node on other end of current_edge, other dart on same edge.
        # I have added a back_node variable here, to see which node has just
        # been left behind. This will be checked later, to see if all four
        # half-darts for this back node have been passed through on self.epath
        
        self.back_node = self.current_node
        self.current_node = self.dart_dict[dart]
        self.current_dart = dart
        
        # Update next available dart list; use original PD code to find index
        # of current_dart, since it may no longer be in dart_adj_dict
        
        loc = self.PD_code[self.current_node].index(self.current_dart)
        
        if abs(self.node_type_dict[self.current_node]) == 1:
            if self.dart_adj_dict[self.current_node][(loc + 2) % 4] != -1:
                self.next_dart_list = [self.PD_code[self.current_node][(loc + 2) % 4]]
        else:
            self.next_dart_list = [dart for dart in self.dart_adj_dict[self.current_node]
                                   if dart != self.current_dart and dart != -1]
            
        #-------------------------------------------------------------------------#
    
    def chooseNextDart(self, next_dart_label):
        """
        This function moves the path along the edge corresponding to
        next_dart_label. Thus,
        it
        
            (1) adds next_dart_label to the temporary Eulerian circuit
            (2) removes the dart from the node being left
            (3) moves the current node to the other side of the edge
            (4) finds all possible darts for the next move
            (5) removes the dart from the current node
            
        """
        
        # Add next dart to temporary Eulerian circuit
            
        self.cpath += [next_dart_label]
        
        # Removes dart as a valid choice from dart_adj_dict, replacing label
        # with -1 to show it has been used in the temporary Eulerian circuit.
        
        loc = self.dart_adj_dict[self.current_node].index(next_dart_label)
        self.dart_adj_dict[self.current_node][loc] = -1
        
        # Finds dart sharing same edge, and makes it current dart; add to cpath
        
        self.current_dart = self.findDartMatch(next_dart_label)
        self.cpath += [self.current_dart]
        
        # Move current node to other side of edge
        
        self.current_node = self.dart_dict[self.current_dart]
        
        # Update next available dart list, then remove dart used to reach this
        # new current node
        
        loc = self.dart_adj_dict[self.current_node].index(self.current_dart)
        
        if abs(self.node_type_dict[self.current_node]) == 1:
            if self.dart_adj_dict[self.current_node][(loc + 2) % 4] != -1:
                self.next_dart_list = [self.dart_adj_dict[self.current_node][(loc + 2) % 4]]
            else:
                self.next_dart_list = []
        else:
            self.next_dart_list = [dart for dart in self.dart_adj_dict[self.current_node]
                                   if dart != self.current_dart and dart != -1]
            
        self.dart_adj_dict[self.current_node][loc] = -1
        
    #-------------------------------------------------------------------------#
            
    def currentNodeDegree(self):
        """
        If current node is a vertex, then all incident edges count; otherwise,
        for a crossing, only the edge opposite the incoming edge.
        """
        
        return len(self.next_dart_list)
    
    #-------------------------------------------------------------------------#
    
    def findDartMatch(self, dart):
        """
        Given a dart label, we find the other dart on the same edge.
        """
        
        # Find the node that the dart is incident to
        
        node = self.dart_dict[dart]
        
        # Find location of outgoing darts by using original node type list
        
        if self.node_type_dict[node] > 0:
            outgoing_list = [2, 3]
        else:
            outgoing_list = [1, 2]
        
        # Find out if this is an incoming or outgoing edge in the original
        # DT sequence by using the PD code
        
        if self.PD_code[node].index(dart) in outgoing_list: # outgoing dart
            return ((dart + 1) % (4 * self.num_node))
        else:                                               # incoming dart
            return (dart - 1) % (4 * self.num_node)
    
    #-------------------------------------------------------------------------#
            
    def lenCPath(self):
        return len(self.cpath)
    
    #-------------------------------------------------------------------------#
            
    def lenEPath(self):
        return len(self.epath)
    
    #-------------------------------------------------------------------------#
        
    def listAvailableDarts(self):
        """
        If current node is a vertex, then all incident edges count; otherwise,
        for a crossing, only the edge opposite the incoming edge.
        """
        
        return self.next_dart_list
            
    #-------------------------------------------------------------------------#
    
    def listCPath(self):
        return self.cpath
    
    #-------------------------------------------------------------------------#
    
    def listCurrentDart(self):
        return self.current_dart
    
    #-------------------------------------------------------------------------#
    
    def listCurrentNode(self):
        return self.current_node
    
    #-------------------------------------------------------------------------#
    
    def listDartAdjDict(self):
        """
        Keys are node labels, values are four-element lists of dart labels
        incident to the given node, or -1 if edge has been used in temporary
        Eulerian circuit
        """
        
        return self.dart_adj_dict
    
    #-------------------------------------------------------------------------#
    
    def listDartDict(self):
        """
        Keys are dart labels, values is node label dart is incident to
        """
        
        return self.dart_dict
    
    #-------------------------------------------------------------------------#
    
    def listEPath(self):
        return self.epath
    
    #-------------------------------------------------------------------------#
    
    def listNodeTypeDict(self):
        return self.node_type_dict
        
    #-------------------------------------------------------------------------#
    
    def listPDCode(self):
        return self.PD_code
        
    #-------------------------------------------------------------------------#
    
    def numNodes(self):
        return self.num_node
        
    #-------------------------------------------------------------------------#
    
    def order(self):
        """
        Since the epath is 'backwards' compared to the original orientation,
        must reverse the PD code appropriately so that it matches e_path
        
        15 Jan 2023: Added code to remove nodes from PD code if the node is
        (1) a vertex that is either (2a) made into a turn in the induced knot
        diagram, or (2b) not, but needs to have its node type changed anyway.
        Also, changed output PD code, so that it is in terms of edges (starting
        at 1, instead of 0, since that is what Sage wants). This code is
        currently commented out.
        
        19 Feb 2023: A global reverse of the PD code does not work in general,
        since the generic Eulerian circuit may lead to different entering
        lower darts for a given node. This depends on how the circuit changes
        direction on portions of the graph, due to improper vertices.
        """
        
        # Put node 0 at beginning of epath
        
        zero = self.epath.index(0)
        self.epath = self.epath[zero:] + self.epath[:zero]
        
        # Process PD code labels for each node, and see how they match the
        # current Eulerian circuit.
        
        num_darts = 4 * self.num_node
        new_PD_code = []
        
        for node in self.PD_code:
            
            # We will keep the current PD code node if it (1) is a proper node,
            # or (2) an improper vertex with the current ingoing dart still an
            # ingoing dart. Note that if the vertex is improper with *both*
            # lower edges as ingoing, this will keep it as is. However, in this
            # case, we will not care about the node type, so it is irrelevant.
            # It will flip the PD code for the vertex if both lower edges are
            # outgoing, but again, this does not matter.
            
            # NOTE: We could check the node type list within the if-else
            # statements below, but I am not worrying about it now. Do we
            # really need to, or is the absolute value of the node type
            # sufficient for later work?
            
            first_label_index = self.epath.index(node[0])
            next_label = self.epath[(first_label_index + 1) % num_darts]
            
            if next_label in node[1:]:
                new_PD_code += [node]
            else:
                new_PD_code += [[node[2], node[3], node[0], node[1]]]
                
        self.PD_code = new_PD_code
    
    #-------------------------------------------------------------------------#
        
    def reverseGraph(self):
        """
        Takes current epath, keeps initial dart in place, and reverses the
        order of the remaining darts; this flips the orientation of all edges.
        
        17 Jul 2022: Since we are using the PD code of the graph, we need to
        reverse this as well. This takes (i j k l) -rev-> (k l i j). The f_list
        should *not* flip sign, since both upper and lower edges reverse
        orientation.
        """
        
        self.epath = [self.epath[0]] + [label for label in self.epath[-1:0:-1]]
        
        self.PD_code = [[code[2], code[3], code[0], code[1]] for code in self.PD_code]
        #self.node_type_dict = {iii : -self.node_type_dict[iii] for iii in self.node_type_dict.keys()}
        
#=============================================================================#

def createCircuits(PD_list, type_list):
    
    # Create the starting graph

    G = Graph(PD_list, type_list)
    
    # Create stack of graphs, intermediate list of graph classes used to
    # find Eulerian circuits through the knotted graph, and the final list of
    # induced knot diagrams
    
    graphStack = [G]
    graphList = []
    
    iter = 0
    
    # Run through DFS of graphs; this finds all possible Eulerian circuits
    # through the knotted graph, and records them in graphList
    
    while len(graphStack) > 0:
        
        # Get next graph
        
        nextGraph = graphStack.pop()
        
        # Print out edge_adj_dict, edge_dict
        
        # If cpath is empty, graph is not placed back into graphStack on any
        # previous iteration, so safe to assume len(cpath) > 0; see if current
        # node has non-zero edges left
        
        if nextGraph.currentNodeDegree() == 0:
            
            # Current node has no remaining edges, pop edge from cpath, add
            # edge to epath; algorithm will now backtrack until it finds node
            # with unused edges
            
            nextGraph.backtrack()
            
            while nextGraph.lenCPath() > 0:
                if nextGraph.currentNodeDegree() > 0:
                    break
                    iter += 1           # How many times is this part of algorithm hit?
                else:
                    nextGraph.backtrack()
                    
            # More processing to be done?
            
            if nextGraph.lenCPath() > 0:
                graphStack += [nextGraph]
            elif nextGraph not in graphList:
                nextGraph.order()
                graphList += [nextGraph]
                
                # Include reversed version of graph circuit
                
                revGraph = deepcopy(nextGraph)
                revGraph.reverseGraph()
                
                graphList += [revGraph]
        
        else:
            
            # Current node has remaining edges in graph; go through
            # all possible darts for current node, and create a
            # new graph for each choice, add to stack
            
            nextList = nextGraph.listAvailableDarts()
            
            for nextDart in nextList:
                newGraph = deepcopy(nextGraph)
                newGraph.chooseNextDart(nextDart)
                graphStack += [newGraph]
            
    # Return results
    
    return graphList
        
#=============================================================================#