'''
############################################################################
############################################################################
#  This program reconstructs a string from the Burrows-Wheeler Transform
#  http://rosalind.info/problems/ba9j/
#
############################################################################
'''
from collections import defaultdict
def parse( fname ):
    return open(fname).read().strip()


def getIndices( c, string ):
    indices = []
    for i, s in enumerate(string):
        if s == c:
            indices.append(i)
    return indices

def reconstruct_BWT( transform ):

    #transform = "ard$rcaaaabb"
    firstColumn = ''.join(sorted(transform)) #lexigraphical ordering of transform

    #get indices for all characters in the string
    indices = { c: getIndices(c, transform) for c in set( transform )}

    #initialize map from first index to last index
    sym_counts = { c: 0 for c in set(firstColumn) }
    imap = []
    for c in firstColumn:

        imap.append( indices[c][sym_counts[c]] )
        sym_counts[c] += 1

    #reconstruct the original string
    original = '$'
    index = transform.index( '$' )

    while len(original) < len(transform):
        original += firstColumn[index]
        index = imap[index]


    return original[1:] + original[0]


def main():
    print(reconstruct_BWT( parse('rosalind_ba9j.txt' ) ))

if __name__ == '__main__':
  main()
