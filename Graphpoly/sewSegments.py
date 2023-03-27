# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 16:35:43 2023

@author: cartin
"""

def sewSegments(e_path, seg_index_1, seg_index_2, start_1, stop_1, start_2, stop_2):
    """
    This function takes two segments in a given e_path, and joins them together
    at the appropriate dart labels. In particular, with the two segments of the
    form
    
        [ab -(1)-][cd -(2)-]
        
    it joins them into a single segment
    
        [ad -(2)- cb -(1)-]
        
    The two parameters seg_index_1 and seg_index_2 give the indices of the
    segments in e_path, where seg_index_1 is the segment containing a, b, and
    seg_index_2 contains c, d. The other variables give the indices of the
    four dart labels a, b, c, d, where
    
        b : start_1
        a : stop_1
        d : start_2
        c : stop_2
        
    The function returns the modified e_path.
    """
    
    seg_1, seg_2 = e_path[seg_index_1], e_path[seg_index_2]
    
    # Find portions of e_path between b, a and d, c; adjust indices
    # so that a, b, c, d are included in new segments
    
    if start_1 < stop_1:
        piece_1 = seg_1[start_1 : stop_1 + 1]
    else:
        piece_1 = seg_1[start_1:] + seg_1[: stop_1 + 1]
        
    if start_2 < stop_2:
        piece_2 = seg_2[start_2 : stop_2 + 1]
    else:
        piece_2 = seg_2[start_2:] + seg_2[: stop_2 + 1]
        
    # Remove current segment, replace with new pieces
    
    e_path.remove(seg_1)
    e_path.remove(seg_2)
    e_path += ([piece_1 + piece_2])
    
    # Return results
    
    return e_path