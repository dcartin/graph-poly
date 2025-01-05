# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 13:28:10 2024

@author: cartin
"""

# Go to graph-poly folder and run "python -m unittest tests.test_LPoly"

import unittest
from Graphpoly import LPoly

class TestLPoly(unittest.TestCase):
    
    #-------------------------------------------------------------------------#
    
    def test_single_cross_unknot(self):
        """
            Unknot with a single crossing
        """
        
        [writhe, state_list] = LPoly([[iii for iii in range(4)]], \
                                     [[0, 3, 1, 2]])
            
        self.assertEqual(writhe, 1)
        self.assertCountEqual(state_list, [(0, 1, 1), (1, 0, 2)])
            
    #-------------------------------------------------------------------------#
    
    def test_single_cross_unknot_relabel(self):
        """
            Unknot with a single crossing, labels shifted by one
        """
        
        [writhe, state_list] = LPoly([[iii for iii in range(4)]], \
                                     [[1, 0, 2, 3]])
            
        self.assertEqual(writhe, 1)
        self.assertCountEqual(state_list, [(0, 1, 1), (1, 0, 2)])
    
    #-------------------------------------------------------------------------#
    
    def test_double_cross_unknot_unlike_type(self):
        """
            Unknot with two crossings, with one overcrossing L to R, and
            the other R to L
        """
        
        [writhe, state_list] = LPoly([[iii for iii in range(8)]], \
                                     [[0, 6, 1, 7], [2, 5, 3, 4]])
            
        self.assertEqual(writhe, 0)
        self.assertCountEqual(state_list, [(1, 1, 1), (0, 2, 2), (2, 0, 2), (1, 1, 3)])

    #-------------------------------------------------------------------------#
    
    def test_double_cross_unknot_like_type(self):
        """
            Unknot with two crossings, with both overcrossings R to L
        """
        
        [writhe, state_list] = LPoly([[iii for iii in range(8)]], \
                                     [[0, 6, 1, 7], [4, 2, 5, 3]])
        
        self.assertEqual(writhe, -2)
        self.assertCountEqual(state_list, [(2, 0, 1), (1, 1, 2), (1, 1, 2), (0, 2, 3)])

    #-------------------------------------------------------------------------#
    
    def test_left_trefoil(self):
        """
            Left trefoil with standard label convention
        """
        
        [writhe, state_list] = LPoly([[iii for iii in range(12)]], \
                                     [[0, 6, 1, 7], [4, 10, 5, 11], [8, 2, 9, 3]])
            
        self.assertEqual(writhe, -3)
        self.assertCountEqual(state_list, [(0, 3, 2), (1, 2, 1), (1, 2, 1), (1, 2, 1), \
                                           (2, 1, 2), (2, 1, 2), (2, 1, 2), (3, 0, 3)])
            
    #-------------------------------------------------------------------------#
            
    def test_right_trefoil(self):
        """
            Right trefoil with standard label convention
        """
        
        [writhe, state_list] = LPoly([[iii for iii in range(12)]], \
                                     [[2, 9, 3, 8], [6, 1, 7, 0], [10, 5, 11, 4]])
            
        self.assertEqual(writhe, 3)
        self.assertCountEqual(state_list, [(0, 3, 3), (1, 2, 2), (1, 2, 2), (1, 2, 2), \
                                            (2, 1, 1), (2, 1, 1), (2, 1, 1), (3, 0, 2)])
             
     #-------------------------------------------------------------------------#