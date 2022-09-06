# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 09:21:50 2019

@author: cartin
"""

def properPair(pair_list, modulus):
    """
    Check whether the two numbers in pair_list are separated
    by more than one mod the given modulus, and are *not*
    separated by two (i.e. both odd or both even).
    
    SHOULD IT BE THAT DIFF IS EVEN, NOT JUST GREATER THAN ONE,
    AND WHY CHECK SECOND ITEM IS ODD?
    """
    
    diff = abs(pair_list[0] - pair_list[1])
    
    if diff > 1 and diff < (modulus - 1):
        if pair_list[1] % 2 == 0 or diff % 2 == 0:
            print(pair_list)
        return True
    else:
        return False
    
#    if diff > 1 and diff < (modulus - 1) and pair_list[1] % 2 == 1:
#        return True
#    else:
#        return False