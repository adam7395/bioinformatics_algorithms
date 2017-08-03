'''
############################################################################
############################################################################
#  This program takes a DNA string and transcribes rna to solve rosalind
#  http://rosalind.info/problems/rna/
#
############################################################################
'''

def parse( fname ):
    with open(fname) as f:
        print( f.readlines())

def transcribe( seq ):
    return seq.upper().replace('T', 'U')

def main():
  print( transcribe( parse( 'rosalind_rna.txt' )))

if __name__ == '__main__':
  main()
