# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 11:17:29 2023

@author: cartin
"""

def splitSegment(e_path, seg_index, start_1, stop_1, start_2, stop_2):
    """
    This function takes a particular segment of a given e_path, and splits the
    segment in two at given locations. In particular, with a segment of the form
    
        [ab -(1)- cd -(2)-]
    
    it splits the segment into
    
        [ad -(2)-][cb -(1)-]
    
    The parameter seg_index gives the index of the segment of interest in e_path.
    The other variables give the indices of the four dart labels a, b, c, d, where
    
        b : start_1
        c : stop_1
        d : start_2
        a : stop_2
        
    The function returns the modified e_path.
    """
    
    current_seg = e_path[seg_index]
    
    # Find portions of e_path between b, c and d, a; adjust
    # indices so that a, b, c, d are included in new segments
    
    if start_1 < stop_1:
        piece_1 = current_seg[start_1 : stop_1 + 1]
    else:
        piece_1 = current_seg[start_1:] + current_seg[: stop_1 + 1]
        
    if start_2 < stop_2:
        piece_2 = current_seg[start_2 : stop_2 + 1]
    else:
        piece_2 = current_seg[start_2:] + current_seg[: stop_2 + 1]
        
    # Remove current segment, replace with new pieces
    
    e_path.remove(current_seg)
    e_path += ([piece_1] + [piece_2])
    
    # Return results
    
    return e_path