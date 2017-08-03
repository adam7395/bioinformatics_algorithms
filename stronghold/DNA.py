'''
############################################################################
############################################################################
#  This algorithm counts the frequence of DNA nucleotide in a string from Rosalind
#  http://rosalind.info/problems/dna/
#
############################################################################
'''

def parse():
    with open( 'rosalind_dna.txt' ) as f:
        for line in f:
            return line.strip()

def count_nucleotides( seq ):
    A = str(seq.count('A'))
    C = str(seq.count('C'))
    G = str(seq.count('G'))
    T = str(seq.count('T'))
    return A, C, G, T


def main():
  print( ' '.join(count_nucleotides( parse() )))

if __name__ == '__main__':
  main()
