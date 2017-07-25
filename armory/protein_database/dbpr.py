'''
############################################################################
############################################################################
#  This program access protein database UniProt with a unique ID
#
############################################################################
'''

import requests

pid = open('rosalind_dbpr.txt').read().strip()
url = r"http://www.uniprot.org/uniprot/{}.txt".format(pid)

processes = []
page = requests.get(url).text.split('\n')
for line in page:
    if line.startswith('DR'):
        if line.split()[1].startswith('GO'):
            if line.split()[3].startswith('P'):
                process = line.split(':')[2].split(';')[0]
                processes.append(process)

for process in processes:
    print(process)
