# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 13:28:10 2024

@author: cartin
"""

# Go to graph-poly folder and run "python -m unittest tests.test_connectList"

import unittest
from Graphpoly import connectList

class TestConnectList(unittest.TestCase):
    """
        For all the test cases below, we use assertListEqual for both seg_list
        and connect_list, since the ordering of the elements is important --
        these should match the order of the PD code for the given node. This is
        either d0, d1, d2, d3 for seg_list, or (undercrossing), (overcrossing)
        for connect_list.
    """
    
    #-------------------------------------------------------------------------#
    
    # def test_number_one(self):
    #     [seg_list, connect_list] = connectList([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]], \
    #                                            [2, 1, 3, 0])
            
    #     self.assertListEqual(seg_list, [(0, 2), (0, 1), (0, 3), (0, 0)])
    #     self.assertListEqual(connect_list, [(2, 3), (0, 1)])
    
    #-------------------------------------------------------------------------#
    
    def test_ambiguous(self):
        """
            For this test, the given node and epath are ambiguous, since d1
            comes after d0, and d2 comes before. However, if d0 -> d1 is chosen,
            then d2 and d3 are not adjacent in the epath, so there must be a
            test of both edges before a decision is made.
        """
        
        
        [seg_list, connect_list] = connectList([[7, 8, 6, 5, 4, 3, 2, 1, 0, 11, 10, 9]], \
                                                [2, 1, 3, 0])
            
        self.assertListEqual(seg_list, [(0, 6), (0, 7), (0, 5), (0, 8)])
        self.assertListEqual(connect_list, [(3, 2), (1, 0)])
    
    #-------------------------------------------------------------------------#
    
    """
        There are a total of 36 base cases to consider, based on which dart d0
        is connected to (3 choices), in which order d0 appears (2 choices), the
        ordering choice for the other two darts (2 choices), and finally how
        each of the dart labels appears in the e_path segment, i.e. are they
        adjacent in the list, or at opposite edges of the list? There are only
        3 choices for this, since only one pair can be on opposite edges. Note
        that we are ignoring whether they are in different segments or not; we
        should probably test that, too!
    """

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#
    
    def test_d0123_both_adj(self):
        """
            This tests d0 -> d1, d2 -> d3, with d_01 = d_23 = 1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [0, 1, 2, 3])
            
        self.assertListEqual(seg_list, [(0, 0), (0, 1), (0, 2), (0, 3)])
        self.assertListEqual(connect_list, [(0, 1), (2, 3)])

    #-------------------------------------------------------------------------#
    
    def test_d0123_one_adj_01(self):
        """
            This tests d0 -> d1, d2 -> d3, with d_01 = -11, d_23 = 1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [11, 0, 1, 2])
            
        self.assertListEqual(seg_list, [(0, 11), (0, 0), (0, 1), (0, 2)])
        self.assertListEqual(connect_list, [(11, 0), (1, 2)])

    #-------------------------------------------------------------------------#
    
    def test_d0123_one_adj_02(self):
        """
            This tests d0 -> d1, d2 -> d3, with d_01 = 1, d_23 = -11
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [9, 10, 11, 0])
            
        self.assertListEqual(seg_list, [(0, 9), (0, 10), (0, 11), (0, 0)])
        self.assertListEqual(connect_list, [(9, 10), (11, 0)])

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#
    
    def test_d0132_both_adj(self):
        """
            This tests d0 -> d1, d3 -> d2, with d_01 = 1, d_23 = -1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [0, 1, 3, 2])
            
        self.assertListEqual(seg_list, [(0, 0), (0, 1), (0, 3), (0, 2)])
        self.assertListEqual(connect_list, [(0, 1), (2, 3)])

    #-------------------------------------------------------------------------#
    
    def test_d0132_one_adj_01(self):
        """
            This tests d0 -> d1, d3 -> d2, with d_01 = -11, d_23 = -1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [11, 0, 2, 1])
            
        self.assertListEqual(seg_list, [(0, 11), (0, 0), (0, 2), (0, 1)])
        self.assertListEqual(connect_list, [(11, 0), (1, 2)])

    #-------------------------------------------------------------------------#
    
    def test_d0132_one_adj_02(self):
        """
            This tests d0 -> d1, d3 -> d2, with d_01 = 1, d_23 = 11
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [9, 10, 0, 11])
            
        self.assertListEqual(seg_list, [(0, 9), (0, 10), (0, 0), (0, 11)])
        self.assertListEqual(connect_list, [(9, 10), (11, 0)])

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#
    
    def test_d0213_both_adj(self):
        """
            This tests d0 -> d2, d1 -> d3, with d_02 = d_13 = 1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [0, 2, 1, 3])
            
        self.assertListEqual(seg_list, [(0, 0), (0, 2), (0, 1), (0, 3)])
        self.assertListEqual(connect_list, [(0, 1), (2, 3)])

    #-------------------------------------------------------------------------#
    
    def test_d0213_one_adj_01(self):
        """
            This tests d0 -> d2, d1 -> d3, with d_02 = -11, d_13 = 1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [11, 1, 0, 2])
            
        self.assertListEqual(seg_list, [(0, 11), (0, 1), (0, 0), (0, 2)])
        self.assertListEqual(connect_list, [(11, 0), (1, 2)])

    #-------------------------------------------------------------------------#
    
    def test_d0213_one_adj_02(self):
        """
            This tests d0 -> d2, d1 -> d3, with d_02 = 1, d_13 = -11
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [9, 11, 10, 0])
            
        self.assertListEqual(seg_list, [(0, 9), (0, 11), (0, 10), (0, 0)])
        self.assertListEqual(connect_list, [(9, 10), (11, 0)])

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#
    
    def test_d0231_both_adj(self):
        """
            This tests d0 -> d2, d3 -> d1, with d_02 = 1, d_13 = -1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [0, 3, 1, 2])
            
        self.assertListEqual(seg_list, [(0, 0), (0, 3), (0, 1), (0, 2)])
        self.assertListEqual(connect_list, [(0, 1), (2, 3)])

    #-------------------------------------------------------------------------#
    
    def test_d0231_one_adj_01(self):
        """
            This tests d0 -> d2, d3 -> d1, with d_02 = -11, d_13 = -1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [11, 2, 0, 1])
            
        self.assertListEqual(seg_list, [(0, 11), (0, 2), (0, 0), (0, 1)])
        self.assertListEqual(connect_list, [(11, 0), (1, 2)])

    #-------------------------------------------------------------------------#
    
    def test_d0231_one_adj_02(self):
        """
            This tests d0 -> d2, d3 -> d1, with d_02 = 1, d_13 = 11
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [9, 0, 10, 11])
            
        self.assertListEqual(seg_list, [(0, 9), (0, 0), (0, 10), (0, 11)])
        self.assertListEqual(connect_list, [(9, 10), (11, 0)])

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#
    
    def test_d0312_both_adj(self):
        """
            This tests d0 -> d3, d1 -> d2, with d_03 = d_12 = 1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [0, 2, 3, 1])
            
        self.assertListEqual(seg_list, [(0, 0), (0, 2), (0, 3), (0, 1)])
        self.assertListEqual(connect_list, [(0, 1), (2, 3)])

    #-------------------------------------------------------------------------#
    
    def test_d0312_one_adj_01(self):
        """
            This tests d0 -> d3, d1 -> d2, with d_03 = -11, d_12 = 1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [11, 1, 2, 0])
            
        self.assertListEqual(seg_list, [(0, 11), (0, 1), (0, 2), (0, 0)])
        self.assertListEqual(connect_list, [(11, 0), (1, 2)])

    #-------------------------------------------------------------------------#
    
    def test_d0312_one_adj_02(self):
        """
            This tests d0 -> d3, d1 -> d2, with d_03 = 1, d_12 = -11
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [9, 11, 0, 10])
            
        self.assertListEqual(seg_list, [(0, 9), (0, 11), (0, 0), (0, 10)])
        self.assertListEqual(connect_list, [(9, 10), (11, 0)])

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#
    
    def test_d0321_both_adj(self):
        """
            This tests d0 -> d3, d2 -> d1, with d_03 = 1, d_12 = -1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [0, 3, 2, 1])
            
        self.assertListEqual(seg_list, [(0, 0), (0, 3), (0, 2), (0, 1)])
        self.assertListEqual(connect_list, [(0, 1), (2, 3)])

    #-------------------------------------------------------------------------#
    
    def test_d0321_one_adj_01(self):
        """
            This tests d0 -> d3, d2 -> d1, with d_03 = -11, d_12 = -1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [11, 2, 1, 0])
            
        self.assertListEqual(seg_list, [(0, 11), (0, 2), (0, 1), (0, 0)])
        self.assertListEqual(connect_list, [(11, 0), (1, 2)])

    #-------------------------------------------------------------------------#
    
    def test_d0321_one_adj_02(self):
        """
            This tests d0 -> d3, d2 -> d1, with d_03 = 1, d_12 = 11
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [9, 0, 11, 10])
            
        self.assertListEqual(seg_list, [(0, 9), (0, 0), (0, 11), (0, 10)])
        self.assertListEqual(connect_list, [(9, 10), (11, 0)])

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#
    
    def test_d1023_both_adj(self):
        """
            This tests d1 -> d0, d2 -> d3, with d_01 = -1, d_23 = 1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                                [1, 0, 2, 3])
            
        self.assertListEqual(seg_list, [(0, 1), (0, 0), (0, 2), (0, 3)])
        self.assertListEqual(connect_list, [(0, 1), (2, 3)])

    #-------------------------------------------------------------------------#
    
    def test_d1023_one_adj_01(self):
        """
            This tests d1 -> d0, d2 -> d3, with d_01 = 11, d_23 = 1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [0, 11, 1, 2])
            
        self.assertListEqual(seg_list, [(0, 0), (0, 11), (0, 1), (0, 2)])
        self.assertListEqual(connect_list, [(11, 0), (1, 2)])

    #-------------------------------------------------------------------------#
    
    def test_d1023_one_adj_02(self):
        """
            This tests d1 -> d0, d2 -> d3, with d_01 = -1, d_23 = -11
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [10, 9, 11, 0])
            
        self.assertListEqual(seg_list, [(0, 10), (0, 9), (0, 11), (0, 0)])
        self.assertListEqual(connect_list, [(9, 10), (11, 0)])

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#
    
    def test_d1032_both_adj(self):
        """
            This tests d1 -> d0, d3 -> d2, with d_01 = -1, d_23 = -1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [1, 0, 3, 2])
            
        self.assertListEqual(seg_list, [(0, 1), (0, 0), (0, 3), (0, 2)])
        self.assertListEqual(connect_list, [(0, 1), (2, 3)])

    #-------------------------------------------------------------------------#
    
    def test_d1032_one_adj_01(self):
        """
            This tests d1 -> d0, d3 -> d2, with d_01 = 11, d_23 = -1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [0, 11, 2, 1])
            
        self.assertListEqual(seg_list, [(0, 0), (0, 11), (0, 2), (0, 1)])
        self.assertListEqual(connect_list, [(11, 0), (1, 2)])

    #-------------------------------------------------------------------------#
    
    def test_d1032_one_adj_02(self):
        """
            This tests d1 -> d0, d3 -> d2, with d_01 = -1, d_23 = 11
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [10, 9, 0, 11])
            
        self.assertListEqual(seg_list, [(0, 10), (0, 9), (0, 0), (0, 11)])
        self.assertListEqual(connect_list, [(9, 10), (11, 0)])

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#
    
    def test_d2013_both_adj(self):
        """
            This tests d2 -> d0, d1 -> d3, with d_02 = -1, d_13 = 1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [1, 2, 0, 3])
            
        self.assertListEqual(seg_list, [(0, 1), (0, 2), (0, 0), (0, 3)])
        self.assertListEqual(connect_list, [(0, 1), (2, 3)])

    #-------------------------------------------------------------------------#
    
    def test_d2013_one_adj_01(self):
        """
            This tests d2 -> d0, d1 -> d3, with d_02 = 11, d_13 = 1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [0, 1, 11, 2])
            
        self.assertListEqual(seg_list, [(0, 0), (0, 1), (0, 11), (0, 2)])
        self.assertListEqual(connect_list, [(11, 0), (1, 2)])

    #-------------------------------------------------------------------------#
    
    def test_d2013_one_adj_02(self):
        """
            This tests d2 -> d0, d1 -> d3, with d_02 = -1, d_13 = -11
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [10, 11, 9, 0])
            
        self.assertListEqual(seg_list, [(0, 10), (0, 11), (0, 9), (0, 0)])
        self.assertListEqual(connect_list, [(9, 10), (11, 0)])

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#
    
    def test_d2031_both_adj(self):
        """
            This tests d2 -> d0, d3 -> d1, with d_02 = -1, d_13 = -1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [1, 3, 0, 2])
            
        self.assertListEqual(seg_list, [(0, 1), (0, 3), (0, 0), (0, 2)])
        self.assertListEqual(connect_list, [(0, 1), (2, 3)])

    #-------------------------------------------------------------------------#
    
    def test_d2031_one_adj_01(self):
        """
            This tests d2 -> d0, d3 -> d1, with d_02 = 11, d_13 = -1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [0, 2, 11, 1])
            
        self.assertListEqual(seg_list, [(0, 0), (0, 2), (0, 11), (0, 1)])
        self.assertListEqual(connect_list, [(11, 0), (1, 2)])

    #-------------------------------------------------------------------------#
    
    def test_d2031_one_adj_02(self):
        """
            This tests d2 -> d0, d3 -> d1, with d_02 = 1, d_13 = 11
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [10, 0, 9, 11])
            
        self.assertListEqual(seg_list, [(0, 10), (0, 0), (0, 9), (0, 11)])
        self.assertListEqual(connect_list, [(9, 10), (11, 0)])

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#
    
    def test_d3012_both_adj(self):
        """
            This tests d3 -> d0, d1 -> d2, with d_03 = -1, d_12 = 1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [1, 2, 3, 0])
            
        self.assertListEqual(seg_list, [(0, 1), (0, 2), (0, 3), (0, 0)])
        self.assertListEqual(connect_list, [(0, 1), (2, 3)])

    #-------------------------------------------------------------------------#
    
    def test_d3012_one_adj_01(self):
        """
            This tests d3 -> d0, d1 -> d2, with d_03 = 11, d_12 = 1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [0, 1, 2, 11])
            
        self.assertListEqual(seg_list, [(0, 0), (0, 1), (0, 2), (0, 11)])
        self.assertListEqual(connect_list, [(11, 0), (1, 2)])

    #-------------------------------------------------------------------------#
    
    def test_d3012_one_adj_02(self):
        """
            This tests d3 -> d0, d1 -> d2, with d_03 = -1, d_12 = -11
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [10, 11, 0, 9])
            
        self.assertListEqual(seg_list, [(0, 10), (0, 11), (0, 0), (0, 9)])
        self.assertListEqual(connect_list, [(9, 10), (11, 0)])

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#
    
    def test_d3021_both_adj(self):
        """
            This tests d3 -> d0, d2 -> d1, with d_03 = -1, d_12 = -1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [1, 3, 2, 0])
            
        self.assertListEqual(seg_list, [(0, 1), (0, 3), (0, 2), (0, 0)])
        self.assertListEqual(connect_list, [(0, 1), (2, 3)])

    #-------------------------------------------------------------------------#
    
    def test_d3021_one_adj_01(self):
        """
            This tests d3 -> d0, d2 -> d1, with d_03 = 11, d_12 = -1
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [0, 2, 1, 11])
            
        self.assertListEqual(seg_list, [(0, 0), (0, 2), (0, 1), (0, 11)])
        self.assertListEqual(connect_list, [(11, 0), (1, 2)])

    #-------------------------------------------------------------------------#
    
    def test_d3021_one_adj_02(self):
        """
            This tests d3 -> d0, d2 -> d1, with d_03 = -1, d_12 = 11
        """
        
        [seg_list, connect_list] = connectList([[iii for iii in range(12)]], \
                                               [10, 0, 11, 9])
            
        self.assertListEqual(seg_list, [(0, 10), (0, 0), (0, 11), (0, 9)])
        self.assertListEqual(connect_list, [(9, 10), (11, 0)])

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#