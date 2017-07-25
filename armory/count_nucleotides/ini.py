'''
############################################################################
############################################################################
#  This program gives the nucleotide count of a DNA seqeunce in
    Output: Integers seperated by a space-Order of counts is A C G T
#
############################################################################
'''

with open( 'rosalind_ini.txt' ) as f:
    seq = f.read().rstrip().lower()
    print(seq)
    A =  seq.count('a')
    C =  seq.count('c')
    G =  seq.count('g')
    T =  seq.count('t')

    print( '{} {} {} {}'.format(A, C, G, T))
