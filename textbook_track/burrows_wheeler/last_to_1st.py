'''
############################################################################
############################################################################
#  Generate the Last-to_First Mapping of a String
#  http://rosalind.info/problems/ba9k/
#
#  Given: A string Transform and an integer i
#  Return: The position LastToFirst(i) in FirstColumn in the Burrows-Wheeler
#
############################################################################
'''
from reconstruct_string_from_BWT import reconstruct_BWT, getIndices

def parse( fname ):
    with open( fname ) as f:
        transform = ''
        i = 0
        for line in f:
            if not transform:
                transform = line.strip()
            else:
                i = int( line.strip())
    return transform, i

def last_to_first( transform, i ):
    firstColumn = ''.join(sorted(transform))

    #get indices for all characters in the string
    indices = { c: getIndices(c, transform) for c in set( transform )}

    #initialize map from first index to last index
    sym_counts = { c: 0 for c in set(firstColumn) }
    imap = []
    for c in firstColumn:
        imap.append( indices[c][sym_counts[c]] )
        sym_counts[c] += 1

    firstToLast = { imap[i]: i for i in imap }

    return firstToLast[i]



def main():
  transform, i = parse( 'rosalind_ba9k.txt' )
  print(last_to_first( transform, i ))

if __name__ == '__main__':
  main()
