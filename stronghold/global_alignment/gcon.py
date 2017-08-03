
from collections import defaultdict

def parse( fname ):
    seqs = []
    with open(fname) as f:
        for line in f:
            if line.startswith('>'): continue
            seqs.append( line.strip())

    return seqs[0], seqs[1]


def parseBLOSUM62():
    blosum = {}

    cmap =   []
    with open('BLOSUM62.txt') as f:
        for line in f:

            #get the characters used to build the blossom matrix
            if not cmap:
                cmap = line.strip().split()

                #initialize blosum matrix
                blosum = { c: {} for c in cmap}
                continue

            #build blosum matrix
            for i, c in enumerate(line.strip().split()[1:]):
                s = 'blosum[{}][{}] = {}'.format( line[0], cmap[i], c)

                blosum[line[0]][cmap[i]] = float(c)

    return blosum


#function to return insertion score for i, j index
def insertion_deletion( i, j, g_align, penalty ):
    i_insertion = i - 1
    j_insertion = j
    i_deletion  = i
    j_deletion  = j - 1


    insertion_score = g_align[i_insertion][j_insertion] + penalty
    deletion_score = g_align[i_deletion][j_deletion] + penalty


    return max( insertion_score, deletion_score )

def match_mismatch( i, j, g_align, blosum, seq1, seq2 ):
    return blosum[seq1[i-1]][seq2[j-1]] + g_align[i-1][j-1]

def mark_cell( i, j, g_align, penalty, blosum, seq1, seq2 ):
    gap = insertion_deletion( i, j, g_align, penalty )
    mmm = match_mismatch( i, j, g_align, blosum, seq1, seq2 )
    return max( gap, mmm )


def global_align( seq1, seq2 ):
    penalty = -5
    blosum = parseBLOSUM62()

    #initialize dp matrix
    g_align = [ [0 for i in range( len(seq2) + 1)] for j in range( len(seq1) + 1)]
    g_align[0] = [ -5 * i for i in range(len(g_align[0]))]
    for i, g in enumerate(g_align):
        g[0] = -5 * i


    for i in range( 1, len(seq1) + 1):
        for j in range( 1, len(seq2) + 1):
            #print( 'i: {}, j: {}'.format(i, j))
            g_align[i][j] = mark_cell( i, j, g_align, penalty, blosum, seq1, seq2 )



    for each in g_align:
        s = ''
        for every in each:
            s += '{:<10}'.format(every)
        print(s)

seq1, seq2 = parse( 'rosalind_gcon.txt' )

global_align(seq1, seq2)
