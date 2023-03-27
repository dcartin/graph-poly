# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 14:26:36 2023

@author: cartin
"""

from Graphpoly.connectList import connectList
from Graphpoly.sewSegments import sewSegments
from Graphpoly.splitSegment import splitSegment

def LPoly(e_path, PD_code):
    
    #-------------------------------------------------------------------------#
    
    # Find the writhe number
    
    writhe = 0
    
    for crossing in PD_code:
        [seg_list, connect_list] = connectList(e_path, crossing)
        
        # There should be no reversals of the link by this point,
        # so do not check whether (d2, d0) appears in connect_list?
        
        if (crossing[1], crossing[3]) in connect_list:     # Right-to-left crossing
            writhe -= 1
        elif (crossing[3], crossing[1]) in connect_list:   # Left-to-right crossing
            writhe += 1
    
    # Create queue for results in-process, and final results list for those
    # where all crossings have been reduced to unknots. Format of items in
    # queue is [e_path, PD_code, (A, B)], with A, B the number corresponding
    # to number of A, B splits enacted so far on that link.
    
    linkQueue = [[e_path, PD_code, (0, 0)]]
    finalStateList = []
    
    #-------------------------------------------------------------------------#
    
    # Go through queue, pop off next link, and process
    
    while len(linkQueue) > 0:
        [current_epath, current_PD_code, (A, B)] = linkQueue.pop()
    
        # If no more crossings, compute prefactor using
        # number of unknots (or states), and put on
        # finalStateList
        
        if len(current_PD_code) == 0:
            finalStateList += [(A, B, len(current_epath))]
            continue
        
        # Get next crossing in current link, assign labels to darts
        
        current_crossing = current_PD_code.pop()
        [d0, d1, d2, d3] = current_crossing
        
        # Find the segment and connection lists for current e_path, node
        
        [seg_list, connect_list] = connectList([label for label in current_epath], \
                                               [label for label in current_crossing])
        
        # Due to orientation reversals, the incoming lower
        # dart may be incorrect. Check to see if this has
        # happened, and modify information accordingly.
        
        if (d2, d0) in connect_list:
            d0, d1, d2, d3 = d2, d3, d0, d1
            seg_list[0], seg_list[1], seg_list[2], seg_list[3] = seg_list[2], \
                seg_list[3], seg_list[0], seg_list[1]
    
        # Go through possible cases for next crossing
    
        if (d1, d3) in connect_list:                   # Right-to-left crossing
            
            if seg_list[0][0] == seg_list[1][0]:       # Two edges are in same segment
                
                # Find A portion of function
                
                current_seg = [dart for dart in current_epath[seg_list[0][0]]]
                A_e_path = [seg for seg in current_epath if seg != current_seg]
                
                if seg_list[3][1] < seg_list[0][1]:
                    piece_1 = current_seg[seg_list[3][1] : seg_list[0][1] + 1]
                    piece_1.reverse()
                    piece_2 = current_seg[seg_list[0][1] + 1:] + current_seg[:seg_list[3][1]]
                else:
                    piece_1 = current_seg[seg_list[3][1]:] + current_seg[:seg_list[0][1] + 1]
                    piece_1.reverse()
                    piece_2 = current_seg[seg_list[0][1] + 1 : seg_list[3][1]]
                    
                A_e_path += [piece_1 + piece_2]
                                                
                # Find A^-1 portion of function
                
                B_e_path = splitSegment([seg for seg in current_epath], seg_list[0][0], \
                                       seg_list[2][1], seg_list[1][1], seg_list[3][1], \
                                       seg_list[0][1])
                
            else:                                      # Two edges are in different segments
                
                # Find A portion of function
                
                current_seg = [dart for dart in current_epath[seg_list[0][0]]]
                A_e_path = [seg for seg in current_epath if seg != current_seg]
                            
                current_seg = current_seg[seg_list[2][1]:] + current_seg[:seg_list[2][1]]
                current_seg.reverse()
                A_e_path += [current_seg]
                
                not_found = True
                
                while not_found:
                    for iii in range(len(A_e_path)):
                        if d1 in A_e_path[iii]:
                            not_found = False
                            d1_index = iii
                
                A_e_path = sewSegments(A_e_path, d1_index, len(A_e_path) - 1, \
                                      seg_list[3][1], seg_list[1][1], current_seg.index(d0), \
                                      current_seg.index(d2))
                                                
                # Find A^-1 portion of function
                
                B_e_path = sewSegments([seg for seg in current_epath], seg_list[0][0], seg_list[1][0], \
                                      seg_list[2][1], seg_list[0][1], seg_list[3][1], \
                                      seg_list[1][1])
            
        elif (d3, d1) in connect_list:                 # Left-to-right crossing
            
            if seg_list[0][0] == seg_list[1][0]:       # Two edges are in same segment
                
                # Find A portion of function
                
                A_e_path = splitSegment([seg for seg in current_epath], seg_list[0][0], \
                                       seg_list[2][1], seg_list[3][1], seg_list[1][1], \
                                       seg_list[0][1])
                                                
                # Find A^-1 portion of function
                
                current_seg = [dart for dart in current_epath[seg_list[0][0]]]
                B_e_path = [seg for seg in current_epath if seg != current_seg]
                
                if seg_list[1][1] < seg_list[0][1]:
                    piece = current_seg[seg_list[1][1] : seg_list[0][1] + 1]
                    piece.reverse()
                    current_seg = current_seg[:seg_list[1][1]] + piece + \
                        current_seg[seg_list[0][1] + 1:]
                else:
                    piece = current_seg[seg_list[1][1]:] + current_seg[:seg_list[0][1] + 1]
                    piece.reverse()
                    current_seg = current_seg[seg_list[0][1] + 1 : seg_list[1][1]] + piece
                    
                B_e_path += [current_seg]
                
            else:                                      # Two edges are in different segments
                
                # Find A portion of function
                
                A_e_path = sewSegments([seg for seg in current_epath], seg_list[0][0], seg_list[1][0], \
                                      seg_list[2][1], seg_list[0][1], seg_list[1][1], \
                                      seg_list[3][1])
                                                
                # Find A^-1 portion of function
                
                current_seg = [dart for dart in current_epath[seg_list[0][0]]]
                B_e_path = [seg for seg in current_epath if seg != current_seg]
                            
                current_seg = current_seg[seg_list[2][1]:] + current_seg[:seg_list[2][1]]
                current_seg.reverse()
                B_e_path += [current_seg]
                
                not_found = True
                
                while not_found:
                    for iii in range(len(B_e_path)):
                        if d1 in B_e_path[iii]:
                            not_found = False
                            d1_index = iii
                            
                B_e_path = sewSegments(B_e_path, d1_index, len(B_e_path) - 1, \
                                       seg_list[1][1], seg_list[3][1], current_seg.index(d0), \
                                       current_seg.index(d2))
                
        # Place latest results back on queue
        
        linkQueue += [[A_e_path, [cross for cross in current_PD_code], (A + 1, B)]]
        linkQueue += [[B_e_path, [cross for cross in current_PD_code], (A, B + 1)]]
        
    # Return results
    
    return [writhe, finalStateList]