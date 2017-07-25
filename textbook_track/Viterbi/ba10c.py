'''
############################################################################
############################################################################
#  This is a solution for Rosalind-Textbook track - BA10A
#  http://rosalind.info/problems/ba10c/
############################################################################
'''

#parse the dataset for sequence and transition matrix
def parse():
    sequence = ''
    cmap     = {} #map characters to transmission index
    smap     = {} #map states to matrix index
    emission = []
    tmatrix  = [] # data to return

    with open( 'rosalind_ba10c.txt' ) as f:
        for line in f:
            if line.startswith('-'):
                continue

            line = line.strip()

            if not sequence:
                sequence = line  #store the sequence
                continue

            if not cmap:
                alphabet = line.split() #map characters to index of transition matrix
                for i,c in enumerate(alphabet):
                    cmap[c] = i
                continue

            if not smap:
                alphabet = line.split() #map characters to index of transition matrix
                for i,c in enumerate(alphabet):
                    smap[c] = i
                continue


            if len( emission ) != len(smap):
                if len(line.strip().split()) == len( smap ) + 1:
                    emission.append(list(map( float, line.split()[1:])))
                continue

            if len( tmatrix )!= len(cmap):
                if len(line.strip().split()) == len( cmap ) + 1:
                    tmatrix.append( list(map( float, line.split()[1:])))
                continue


    return sequence, cmap, smap, emission, tmatrix

def Viterbi():
    sequence, cmap, smap, emission, tmatrix = parse()

    #create probability matrix
    viterbi = [ [0 for i in range(len(sequence))] for j in range(len(smap)) ]

    #initialize probabilty matrix
    viterbi[0][0] = .5 * tmatrix[0][cmap[sequence[0]]]
    viterbi[1][0] = .5 * tmatrix[1][cmap[sequence[0]]]



    #build probabilities
    for j in range(1, len(sequence)):
        prev = j - 1

        viterbi[0][j]  = viterbi[0][prev] * emission[0][0] * tmatrix[0][cmap[sequence[j]]]
        viterbi[0][j] += viterbi[1][prev] * emission[1][0] * tmatrix[0][cmap[sequence[j]]]
        viterbi[1][j]  = viterbi[1][prev] * emission[1][1] * tmatrix[1][cmap[sequence[j]]]
        viterbi[1][j] += viterbi[0][prev] * emission[0][1] * tmatrix[1][cmap[sequence[j]]]


    #build hidden path
    path = ''
    for j in range( len(sequence)):
        states = list(smap.keys())


        if viterbi[0][j] >= viterbi[1][j]:
            path += states[0]
        else:
            path += states[1]

    print(path)




Viterbi()
