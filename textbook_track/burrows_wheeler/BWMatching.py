'''
############################################################################
############################################################################
#  Finds the number of occurences of finding a pattern in a text given only
#    the first and last column, the pattern, and the lastToFirst
#    http://rosalind.info/problems/ba9l/
#
#    Given: A string and a collection of patterns
#    Return: A list of integers showing the count for each pattern
#
#
############################################################################
'''

def parse( fname ):
    with open( fname ) as f:
        text = ''
        patterns = []
        for line in f:
            if not text: text = line.strip()
        else: patterns = line.strip().split()
    return text, patterns

def getFirstAndLast( transform ):
    return ''.join(sorted( transform )), transform


def getIndices( c, string ):
    indices = []
    for i, s in enumerate(string):
        if s == c:
            indices.append(i)
    return indices

def BWTransform( sequence ):

    BWT = [ sequence ]
    for i in range(1,  len( sequence ) + 1):
        BWT.append( BWT[i-1][-1] + ''.join(BWT[-1][0:-1]) )

    return ''.join( [row[-1] for row in sorted(BWT[1:])] )

def last_to_first( transform ):
    firstColumn = ''.join(sorted(transform))

    #get indices for all characters in the string
    indices = { c: getIndices(c, transform) for c in set( transform )}

    #initialize map from first index to last index
    sym_counts = { c: 0 for c in set(firstColumn) }
    imap = []
    for c in firstColumn:
        imap.append( indices[c][sym_counts[c]] )
        sym_counts[c] += 1

    lastToFirst = { imap[i]: i for i in range(len(imap)) }


    return lastToFirst

def BWMatching( firstColumn, lastColumn, pattern, lastToFirst ):

    #initialize the indices
    top = 0
    bottom = len( lastColumn ) - 1

    #terminate if no matches exist
    while top <= bottom:

        #while there are symbols in pattern to be matched
        if pattern:
            symbol = pattern[-1] #store the last symbol
            pattern = pattern[0:-1] #remove last symbol


            topIndex, bottomIndex = (0, 0)
            if symbol in lastColumn[top: bottom + 1]:
                topFound = False
                for i in range( top, bottom + 1):
                    if symbol == lastColumn[i]:
                        if not topFound:
                            topFound = True
                            topIndex = i
                        else:
                            bottomIndex = i


                top = lastToFirst[topIndex]
                if bottomIndex == 0:
                    bottom = top
                else:
                    bottom = lastToFirst[bottomIndex]
            else:
                return 0





        else:
            #print('returning: bottom: {}, top: {}'.format(bottom, top))
            return bottom - top + 1






def main():
    text, patterns = parse( 'rosalind_ba9l.txt' )
    #text = 'panamabananas$'
    #transform = BWTransform( text )
    firstColumn, lastColumn = getFirstAndLast( text )


    lastToFirst = last_to_first( lastColumn )

    counts = [ str(BWMatching( firstColumn, lastColumn, pattern, lastToFirst )) for pattern in patterns]

    with open( 'output/rosalind_ba9l.txt', 'w'  ) as f:
        f.write( ' '.join(counts))



if __name__ == '__main__':
  main()

#$aaaaaabmnnnps
#smnpbnnaaaaa$a
"""
i: 0, v: 12
i: 1, v: 7
i: 2, v: 8
i: 3, v: 9
i: 4, v: 10
i: 5, v: 11
i: 6, v: 13
i: 7, v: 4
i: 8, v: 1
i: 9, v: 2
i: 10, v: 5
i: 11, v: 6
i: 12, v: 3
i: 13, v: 0
"""
#$AAAAAAAAAAAAAACCCCCCCCCCCCCCCGGGGGGTTTTTTTTTTTTTTT
#ACCGAAAGAGGTTTATCATTTACTTCTGCCT$TAGCCCCTCACTCTAACAA
