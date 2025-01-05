# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 13:28:10 2024

@author: cartin
"""

# Go to graph-poly folder and run "python -m unittest tests.test_notComposite"

import unittest
from Graphpoly import notComposite

class TestNotComposite(unittest.TestCase):

    #-------------------------------------------------------------------------#
    
    def test_negative_values(self):
        """
            Sequence contains negative values
        """
        
        orig_seq = [[0, 5], [2, -1], [4, 7], [6, 3], [8, 9], [10, 1]]
        
        self.assertRaises(ValueError, notComposite, orig_seq)

    #-------------------------------------------------------------------------#
    
    def test_exceed_size(self):
        """
            Sequence contains label greater than 2N - 1
        """
        
        orig_seq = [[0, 11], [2, 7], [4, 13], [6, 9], [8, 3], [10, 5]]
        
        self.assertRaises(ValueError, notComposite, orig_seq)
    
    #-------------------------------------------------------------------------#
    
    def test_missing_labels(self):
        """
            Sequence is missing labels; all other constraints satisfied
        """
        
        orig_seq = [[0, 7], [2, 11], [4, 3], [8, 5], [10, 13]]
        
        self.assertRaises(ValueError, notComposite, orig_seq)
    
    #-------------------------------------------------------------------------#
    
    def test_extra_labels(self):
        """
            Sequence has extra labels; all other constraints satisfied
        """
        
        orig_seq = [[0, 13], [2, 7], [4, 7], [6, 5], [6, 3], [8, 11], [10, 9]]
        
        self.assertRaises(ValueError, notComposite, orig_seq)
    
    #-------------------------------------------------------------------------#
    
    def test_wrong_node_order(self):
        """
            At least one node has order [odd, even]
        """
        
        orig_seq = [[0, 11], [2, 7], [4, 5], [13, 6], [8, 9], [10, 3]]
        
        self.assertRaises(ValueError, notComposite, orig_seq)
        
    #-------------------------------------------------------------------------#
    
    def test_prime_seq(self):
        """
            Prime sequence; return original sequence without change
        """
        
        orig_seq = [[0, 5], [2, 9], [4, 7], [6, 3], [8, 11], [10, 1]]
        result = notComposite(orig_seq)
            
        self.assertListEqual(orig_seq, result[0])
    
    #-------------------------------------------------------------------------#
    
    def test_initial_self_loop_1(self):
        """
            Initial self-loop of form (0, 1)
        """
        
        orig_seq = [[0, 1], [2, 3], [4, 9], [6, 7], [8, 5], [10, 11]]
        
        result = notComposite(orig_seq)
        result = result[0] + [[(label + 2 * len(result[0])) for label in node] for node in result[1]]
            
        self.assertListEqual(orig_seq, result)
    
    #-------------------------------------------------------------------------#
    
    def test_initial_self_loop_2(self):
        """
            Initial self-loop of form (0, 2N - 1)
        """
        
        orig_seq = [[0, 11], [2, 5], [4, 9], [6, 3], [8, 1], [10, 7]]
        final_seq = [[0, 7], [2, 5], [4, 1], [6, 9], [8, 3], [10, 11]]
        
        result = notComposite(orig_seq)
        result = result[0] + [[(label + 2 * len(result[0])) for label in node] for node in result[1]]
            
        self.assertListEqual(final_seq, result)
    
    #-------------------------------------------------------------------------#
    
    def test_initial_perm(self):
        """
            Initial perm of >1 nodes, starts at 0; reconstructs original sequence
        """
        
        # NOTE: There is no need to have a separate test for a final
        # subpermutation, i.e. ending on the label 2N - 1, since this test
        # should catch that situation. The procedure notComposite() will never
        # return a final subperm as the first sequence it finds.
        
        orig_seq = [[0, 3], [2, 5], [4, 1], [6, 9], [8, 11], [10, 7]]
        
        result = notComposite(orig_seq)
        result = result[0] + [[(label + 2 * len(result[0])) for label in node] for node in result[1]]
            
        self.assertListEqual(orig_seq, result)
    
    #-------------------------------------------------------------------------#
    
    def test_internal_self_loop_1(self):
        """
            Self-loop of form (2k, 2k + 1), 0 < k < N
        """
        
        orig_seq = [[0, 11], [2, 3], [4, 7], [6, 9], [8, 5], [10, 1]]
        final_seq = [[0, 1], [2, 5], [4, 7], [6, 3], [8, 11], [10, 9]]
        
        result = notComposite(orig_seq)
        result = result[0] + [[(label + 2 * len(result[0])) for label in node] for node in result[1]]
            
        self.assertListEqual(final_seq, result)
    
    #-------------------------------------------------------------------------#
    
    def test_internal_self_loop_2(self):
        """
            Self-loop of form (2k, 2k - 1), 0 < k < N
        """
        
        orig_seq = [[0, 3], [2, 7], [4, 11], [6, 5], [8, 1], [10, 9]]
        final_seq = [[0, 1], [2, 9], [4, 5], [6, 11], [8, 3], [10, 7]]
        
        result = notComposite(orig_seq)
        result = result[0] + [[(label + 2 * len(result[0])) for label in node] for node in result[1]]
            
        self.assertListEqual(final_seq, result)
    
    #-------------------------------------------------------------------------#
    
    def test_internal_perm_1(self):
        """
            Subpermutation not involving initial or final nodes, starts on odd
        """
        
        orig_seq = [[0, 9], [2, 11], [4, 7], [6, 3], [8, 5], [10, 1]]
        final_seq = [[0, 3], [2, 5], [4, 1], [6, 9], [8, 11], [10, 7]]
        
        result = notComposite(orig_seq)
        result = result[0] + [[(label + 2 * len(result[0])) for label in node] for node in result[1]]
            
        self.assertListEqual(final_seq, result)
    
    #-------------------------------------------------------------------------#
    
    def test_internal_perm_2(self):
        """
            Subpermutation not involving initial or final nodes, starts on even
        """
        
        orig_seq = [[0, 11], [2, 7], [4, 9], [6, 3], [8, 5], [10, 1]]
        final_seq = [[0, 5], [2, 7], [4, 1], [6, 3], [8, 11], [10, 9]]
        
        result = notComposite(orig_seq)
        result = result[0] + [[(label + 2 * len(result[0])) for label in node] for node in result[1]]
            
        self.assertListEqual(final_seq, result)
    
    #-------------------------------------------------------------------------#