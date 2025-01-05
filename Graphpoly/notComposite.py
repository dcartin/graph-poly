# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 09:19:14 2019

@author: cartin

05 Jan 2025: This code was substantially rewritten, to (1) ensure that all
subpermutations were being checked, and (2) to allow for the two subpermutations
to be returned. The latter is so that we can run the DT algorithm on each
subpermutation, and find the corresponding f(i) function.

TO DO: When searching for all N(N - 1) subpermutations to look for in an N node
sequence, the computer does a brute-force search for these ranges. However, the
comments describe which ranges they should find, so we can code these in. I
just have not done this.
"""

def notComposite(sequence: list[list[int, int]], return_components: bool = True) -> list | bool:
    """
        Determine whether a DT sequence is a composite permutation or not.
    """

    num_nodes = len(sequence)
    sequence.sort()
    
    # The sequence should be composed of integer label pairs of the form
    # [2j, 2k + 1] where 0 <= j, k < len(seq), given in sorted order. The
    # sorting has already been dealt with; since the remaining facts are
    # assumed below, we test that they are correct for the sequence provided.

    label_list = [label for node in sequence for label in node]
    
    if set([iii for iii in range(2 * num_nodes)]) != set(label_list):
        raise ValueError('Missing or extra labels in sequence of integers')
        
    min_label, max_label = min(label_list), max(label_list)
    
    if min_label < 0:
        raise ValueError('Sequence should not contain negative values')
        
    if max_label > 2 * num_nodes:
        raise ValueError('Sequence labels should be less than {}'.format(2 * num_nodes))
    
    if not all([((node[0] % 2 == 0) and (node[1] % 2 == 1)) for node in sequence]):
        raise ValueError('Incorrect order for node labels')
        
    # From this point on, crossing information is not necessary, so filter out
    # this information (if present) and redefine sequence only in terms of its
    # raw DT labels.
    
    sequence = [[sequence[iii][0], sequence[iii][1]] for iii in range(num_nodes)]
    
    # 04 Jan 2025:
    # 
    # This program has been completed reworked since I initially wrote it. Here
    # is the theory behind it. For starters, for proper subsequences of N nodes,
    # there are 2N(N - 1) such subsequences -- this seems to be a typo in
    # Dowker and Thistletwaite -- where there are 2N choices for the starting
    # value, and N - 1 choices for length, i.e. 2, 4, ..., 2(N - 1). Since
    # if a subsequence maps to itself under i -> a(i), so does its complement,
    # we only need to consider N(N - 1) total sequences. We now try to choose
    # these wisely.
    
    # First, it simplifies the programming if we do not allow sequences where
    # the label 0 appears anywhere but in the initial position. This is the
    # same as forbidding sequences to 'wrap around' from end to start, so that
    # we are looking solely for sequences in between the values 0, 2N - 1. For
    # each choice of k node sequences, there are 2k - 1 such forbidden
    # subsequences: there are 2k labels, and so 2k - 1 choices for where the 0
    # label goes. For proper sequences, then we are looking at 1 + 3 + ... +
    # 2(N - 1) - 1 total sequences we do not allow. This is the sum of the
    # first (N - 1) odd numbers, so the total number is (N - 1)^2.
    
    # We want a total of N(N - 1) sequences, and since
    #
    #   N(N - 1) - (N - 1)^2 = N - 1
    #
    # then there are this many additional sequences we can remove from the
    # final list.
    
    # If N is odd, then there are 2 unnecessary sequences for each of the
    # values 2(N - 1), 2(N - 3), ... N + 1. These sequences of length k can be
    # reduced down to a smaller length (2N - k). These are
    #
    #   [0, 1, 2, ..., 2N - 3] -> [2N - 2, 2N - 1]
    #   [2, 3, 4, ..., 2N - 1] -> [0, 1]
    #
    #   [0, 1, 2, ..., 2N - 5] -> [2N - 4, 2N - 3, 2N - 2, 2N - 1]
    #   [4, 5, 6, ..., 2N - 1] -> [0, 1, 2, 3]
    #
    #   ...
    #
    # and so forth. The arrows show the equivalent, smaller sequence. Note that
    # either decreasing the label of the first sequence in each pair by 1 gives
    # a forbidden sequence after the substitution, while increasing that of the
    # second by 1, gives forbidden sequences gives one before the substitution,
    # so these sequences form the 'boundaries' of these sets. These are the
    # longer sequences that need to be kept to avoid forbidden sequences of
    # smaller length. Thus, for example, the sequence
    #
    #   [1, 2, ..., 2N - 2]
    #   
    # takes the place of [2N - 1, 0]. As shown above, there will be (N - 1)^2
    # of these longer sequences.
    
    # If N is even, there is in addition a N node sequence unnecessary due to
    # symmetry, which can be replaced by another N node sequence given by
    #
    #   [N, N + 1, ..., 2N - 1] -> [0, 1, 2, ..., N - 1]
    
    temp_list = []
    test_seq_list = []
    
    for kkk in range(1, num_nodes):
        temp_list += [[iii for iii in range(jjj, jjj + 2 * kkk)] \
                      for jjj in range(2 * (num_nodes - kkk) + 1)]
            
    for temp in temp_list:
        minus = [iii for iii in range(2 * num_nodes) if iii not in temp]
        flag = False
        
        for other in temp_list:
            if temp != other and set(other) == set(minus) and (len(temp) > len(other) or \
                (len(temp) == len(other) and temp > other)):
                    flag = True
                    break
                
        if not flag:
            test_seq_list += [temp]
    
    flag = False
            
    for test_seq in test_seq_list:
        
        # Since all of the test sequences are sorted, if the first label L_0 is
        # even, then we only need to compare it starting with the node L_0 / 2.
        # If L_0 is odd, then it could be for the nodes ceil(L_0 / 2). Note that
        # we do not need to look at ceil(L_0 / 2) - 1, since for every test_seq
        # starting with [2N + 1, 2N + 2, ...], which catches all ceil(L_0 / 2)
        # cases, there is another one with [2N - 1, 2N, ...], which catches the
        # others.
        
        first = test_seq[0]
        test_len = len(test_seq)
        
        if first % 2 == 0:
            
            start, stop = first // 2, (first + test_len) // 2
            compare_seq = sorted([label for pair in sequence[start : stop] for label in pair])
                
            if test_seq == compare_seq:
                flag = True
                break
                
        else:
            
            start, stop = (first + 1) // 2, (first + test_len + 1) // 2
            compare_seq = sorted([label for pair in sequence[start : stop] for label in pair])
                
            if test_seq == compare_seq:
                flag = True
                break
        
    if flag:
        
        # The sequence does not necessary start at the first even label, so
        # we find this using the minimum size label in the sequence, and
        # subtract this off all labels. Then we ensure the nodes are in the
        # proper form (even, odd) and sort.
            
        first_seq = [label for node in sequence[start: start + (test_len // 2)] for label in node]
        
        min_label = min(first_seq)
        found_seq = [[(label - min_label) % (2 * num_nodes) for label in node] \
                     for node in sequence[start: start + (test_len // 2)]]
            
        found_seq = sorted([[node[0], node[1]] if node[0] % 2 == 0 else [node[1], node[0]] \
                            for node in found_seq])
        
        # For the rest of the sequence, we want to split them apart in such a
        # way that that they can easily be put back together. We do this by
        # starting at the node "to the right" of found_seq. We find the largest
        # label max_label in found_seq, then subtract (max_label + 1) from all
        # labels in the second sequence, mod the length of the original sequence.
        # Since we are taking the mod, these numbers will all be less than twice
        # the number of nodes in this new, second sequence. Then, we sort to
        # ensure all nodes have correct (even, odd) form, and overall ordering.
        
        # To perhaps reiterate a point, the labels first_seq found by the
        # algorithm above will never be made of labels [2k - 1, 2N - 1] +
        # [0, 2j - 1], since this would be a forbidden sequence. Thus, we
        # always have labels in the range [2j, 2k - 1] for j < k, and max_label
        # will then be 2k - 1. There will be no issue with max_label, since the
        # sequence first_seq does not "wrap around zero".
        
        max_label = max(first_seq)
        
        other_seq = [[(label - max_label - 1) % (2 * num_nodes) for label in node] \
                     for node in sequence[start + (test_len // 2) :] + sequence[: start]]
        
        other_seq = sorted([[node[0], node[1]] if node[0] % 2 == 0 else [node[1], node[0]] \
                     for node in other_seq])
                     
        # From this, we have two sequences found_seq and other_seq, and the original
        # sequence (or really, a sequence isomorphic to the original) can be
        # reconstructed by found_seq + other_seq, appropriately relabeling the
        # values in other_seq.
            
        if return_components:
            return [found_seq, other_seq]
        else:
            return False
        
    else:
        if return_components:
            return [sequence]
        else:
            return True