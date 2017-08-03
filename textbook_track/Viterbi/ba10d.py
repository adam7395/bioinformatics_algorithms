'''
############################################################################
############################################################################
#  This is a solution for Rosalind-Textbook track - BA10A
#  http://rosalind.info/problems/ba10d/
#
############################################################################
'''

from ba10c import parse



def Viterbi_probability():
    sequence, cmap, smap, tmatrix, emission = parse('rosalind_ba10d.txt')

    #initialize probability matrix
    pmatrix = [ [ 1 for i in range(len(sequence))] for j in range(len(smap))]

    #base case
    pmatrix[0][0] = .5 * emission[0][cmap[sequence[0]]]
    pmatrix[1][0] = .5 * emission[1][cmap[sequence[0]]]




    #build the pmatrix using dynamic programming
    for i in range( 1, len( sequence ) ):

        p1 = pmatrix[0][i-1] * tmatrix[0][0] * emission[0][cmap[sequence[i]]]
        p2 = pmatrix[1][i-1] * tmatrix[1][0] * emission[0][cmap[sequence[i]]]
        pmatrix[0][i] = p1 + p2

        p1 = pmatrix[0][i-1] * tmatrix[0][1] * emission[1][cmap[sequence[i]]]
        p2 = pmatrix[1][i-1] * tmatrix[1][1] * emission[1][cmap[sequence[i]]]
        pmatrix[1][i] = p1 + p2


    print( pmatrix[0][-1] + pmatrix[1][-1] )






def main():
  Viterbi_probability()

if __name__ == '__main__':
  main()
