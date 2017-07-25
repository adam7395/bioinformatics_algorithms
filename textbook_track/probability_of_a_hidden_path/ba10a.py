'''
############################################################################
############################################################################
#  This is a solution for Rosalind-Textbook track - BA10A
#  http://rosalind.info/problems/ba10a/
#
############################################################################
'''

#parse the dataset for sequence and transition matrix
def parse():
    sequence = ''
    cmap     = {}
    tmatrix  = [] # data to return

    with open( 'rosalind_ba10a.txt' ) as f:
        for line in f:
            if line.startswith('-'): continue

            line = line.strip()

            if not sequence:
                sequence = line  #store the sequence
                continue

            if not cmap:
                alphabet = line.split() #map characters to index of transition matrix
                for i,c in enumerate(alphabet):
                    cmap[c] = i
                continue

            if len(line.split()) != 3: continue
            else:
                tmatrix.append( list( map( float, line.split()[1:])))  #store transition probabilities

    return sequence, cmap, tmatrix



def solve():
    p = .5 #initialize the probability assuming A,B are equal to start
    sequence, cmap, tmatrix = parse()

    current = sequence[0]
    for c in sequence[1:]:
        index1 = cmap[current]
        index2 = cmap[c]
        current = c
        p *= tmatrix[index1][index2]

    return p


print(solve())
