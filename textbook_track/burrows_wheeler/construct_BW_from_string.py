'''
############################################################################
############################################################################
#  This program constructs the Burrows-Wheeler Transform of a string
#  http://rosalind.info/problems/ba9i/
#
############################################################################
'''

def parse( fname ):
    return open(fname).read().strip()

def BWTransform( sequence ):

    BWT = [ sequence ]
    for i in range(1,  len( sequence ) + 1):
        BWT.append( BWT[i-1][-1] + ''.join(BWT[-1][0:-1]) )

    return ''.join( [row[-1] for row in sorted(BWT[1:])] )

def main():
  print(BWTransform( parse( 'rosalind_ba9i.txt' )))


if __name__ == '__main__':
  main()
