'''
############################################################################
############################################################################
#  This is a solution for Rosalind-Textbook track - BA10B
#  http://rosalind.info/problems/ba10b/
#
############################################################################
'''


def parse():
    x = ''
    pi = ''
    cmapx = {}
    cmap_pi = {}
    tmatrix = [] #data to return

    with open( 'rosalind_ba10b.txt') as f:
        for line in f:
            if line.startswith('-'): continue
            line = line.strip()

            if not x:
                x = line #store the sequence of x
                continue

            if not cmapx:
                alphabet = line.split()  #map x chars to transition columns
                for i, c in enumerate(alphabet):
                    if not c: continue
                    cmapx[c] = i
                continue

            if not pi:
                pi = line #store the hidden path
                continue

            if not cmap_pi:
                alphabet = line.split()  #map pi chars to transition rows
                for i, c in enumerate(alphabet):
                    if not c: continue
                    cmap_pi[c] = i
                    continue

            if len(line.split()) != 4: continue

            else:
                tmatrix.append( list( map( float, line.split()[1:])))  #store transition probabilities


    return x, pi, cmapx, cmap_pi, tmatrix


def solve():
    x, pi, cmapx, cmap_pi, tmatrix = parse()

    p = 1 #initialize probability

    for i, c in enumerate(x):
        index2 = cmapx[c]
        index1 = cmap_pi[pi[i]]

        p *= tmatrix[index1][index2]

    return p



print(solve())
