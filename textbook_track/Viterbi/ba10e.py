
import sys, os, re
import math

def prob(path, transition):
    p = 0.5
    for i in xrange(len(path)-1):
        p *= transition[(path[i],path[i+1])]
    return p


def emitt_prob(string, path, emission):
    prob = 1
    for i in xrange(len(string)):
        prob *= emission[(path[i], string[i])]
    return prob

def decoding(string, states, transition, emission):
    p = 1
    dic = {}

    dic[0] = {}
    for i in states:
        dic[0][i] = {}
        dic[0][i]['p'] = 1.0/len(states)*emission[i][string[0]]
    for i in xrange(1,len(string)):
        dic[i] = {}
        for j in states:
            dic[i][j] = {}
            max_value = -1
            pre_state = ''
            for k in states:
                p_value = dic[i-1][k]['p']*transition[k][j]*emission[j][string[i]]
                if p_value > max_value:
                    max_value = p_value
                    pre_state = k
            dic[i][j]['p'] = max_value
            dic[i][j]['pre_state'] = pre_state

    res = ''
    max_value = -1
    max_state = ''
    for i in states:
        if dic[len(string)-1][i]['p']>max_value:
            max_value = dic[len(string)-1][i]['p']
            max_state = i
    res = max_state+res
    for i in xrange(len(string)-1,0,-1):
        max_state = dic[i][max_state]['pre_state']
        res = max_state+res

    return res

def profile_hmm(thresh, alphabet, alignment):

    ##### first label all states, then cal
    thresh = thresh * len(alignment)
    states = []
    insert_index = []
    for i in xrange(len(alignment[0])):
        total = 0
        for j in alignment:
            if j[i] == '-':
                total += 1
        if total > thresh:
            insert_index.append(i)

    emission = {}
    emission['S'] = dict((x,0) for x in alphabet)
    emission['E'] = dict((x,0) for x in alphabet)
    emission['I0'] = dict((x,0) for x in alphabet)
    for i in xrange(1,len(alignment[0])-len(insert_index)+1):
        emission['I'+str(i)] = dict((x,0) for x in alphabet)
        emission['M'+str(i)] = dict((x,0) for x in alphabet)
        emission['D'+str(i)] = dict((x,0) for x in alphabet)

    for i in xrange(len(alignment)):
        per_state = []
        current_index = 1
        for j in xrange(len(alignment[i])):
            if j not in insert_index:
                if alignment[i][j] == '-':
                    per_state.append('D'+str(current_index))
                else:
                    per_state.append('M'+str(current_index))
                    emission['M'+str(current_index)][alignment[i][j]] += 1
                current_index += 1
            else:
                if alignment[i][j]!='-':
                    per_state.append('I'+str(current_index-1))
                    emission['I'+str(current_index-1)][alignment[i][j]] += 1
        states.append(per_state)

    for key in emission:
        total = 0
        for sub_key in emission[key]:
            total += emission[key][sub_key]
        for sub_key in emission[key]:
            if total > 0:
                emission[key][sub_key] = 1.0*emission[key][sub_key]/total
            else:
                emission[key][sub_key] = 0
    transition = {}
    transition['S']={}
    transition['S']['I0'] = 0
    transition['S']['D1'] = 0
    transition['S']['M1'] = 0
    for i in states:
        transition['S'][i[0]] += 1
    transition['I0']={}
    transition['I0']['I0'] = 0
    transition['I0']['D1'] = 0
    transition['I0']['M1'] = 0
    # for i in states:
    #     transition['I0'][i[0]] += 1

    for i in xrange(len(states)):
        for j in xrange(len(states[i])-1):
            if states[i][j] not in transition:
                transition[states[i][j]] = {}
            if states[i][j+1] not in transition[states[i][j]]:
                transition[states[i][j]][states[i][j+1]] = 0
            transition[states[i][j]][states[i][j+1]] += 1
        if not states[i][len(states[i])-1] in transition:
            transition[states[i][len(states[i])-1]] = {}
        if not 'E' in transition[states[i][len(states[i])-1]]:
            transition[states[i][len(states[i])-1]]['E'] = 0
        transition[states[i][len(states[i])-1]]['E'] += 1

    for key in transition:
        total = 0
        for sub_key in transition[key]:
            total += transition[key][sub_key]
        for sub_key in transition[key]:
            if total > 0:
                transition[key][sub_key] = 1.0*transition[key][sub_key]/total
            else:
                transition[key][sub_key] = 0


    ##### print transition table
    index_list = ['S', 'I0']
    for i in xrange(1,len(alignment[0])-len(insert_index)+1):
        index_list.extend(['M'+str(i), 'D'+str(i), 'I'+str(i)])
    index_list.append('E')
    print ' ',
    for i in index_list:
        print i,
    print
    for i in index_list:
        print i,
        if i in transition:
            for j in index_list:
                if j in transition[i]:
                    print round(transition[i][j],3),
                else:
                    print 0,
            print
        else:
            for j in index_list:
                print 0,
            print

    print '--------'









    ##### print emission table
    print ' ',
    for i in alphabet:
        print i,
    print
    print 'S',
    for i in alphabet:
        print round(emission['S'][i],3),
    print
    print 'I0',
    for j in alphabet:
        print round(emission['I0'][j],3),
    print

    # print ' '.join([str(x) for x in dict(sorted(emission['I0'].items())).values()])
    for i in xrange(1,len(alignment[0])-len(insert_index)+1):

        print 'M'+str(i),
        for j in alphabet:
            print round(emission['M'+str(i)][j],3),
        print

        print 'D'+str(i),
        for j in alphabet:
            print round(emission['D'+str(i)][j],3),
        print
        print 'I'+str(i),
        for j in alphabet:
            print round(emission['I'+str(i)][j],3),
        print



    print 'E',
    for j in alphabet:
        print round(emission['E'][j],3),
    print








    # insert_index = []
    # thresh = thresh * len(alignment)
    # transition = {}
    # emission = {}
    # for i in xrange(len(alignment[0])):
    #     total = 0
    #     for j in alignment:
    #         if j[i] == '-':
    #             total += 1
    #     if total > thresh:
    #         insert_index.append(i)
    # state_index = -1
    # transition['S'] = {}
    # transition['I0'] = {}
    # emission['I0'] = dict((x,0) for x in alphabet)
    # tmp_index = 0
    # transition['S']['I0'] = 0
    # transition['I0']['I0'] = 0

    # while tmp_index in insert_index:
    #     for m in xrange(len(alignment)):
    #         if alignment[m][tmp_index] != '-':
    #             if tmp_index == 0:
    #                 transition['S']['I0'] += 1
    #             else:
    #                 transition['I0']['I0'] += 1

    #             emission['I0'][alignment[m][tmp_index]] += 1
    #     tmp_index += 1

    # transition['I0']['I0'] = 1.0*transition['I0']['I0']/((tmp_index-1)*len(alignment)) if tmp_index-1>0 else 0
    # transition['S']['I0'] = 1.0*transition['S']['I0']/len(alignment)
    # for key in alphabet:
    #     emission['I0'][key] = 1.0*emission['I0']['key']/sum(emission['I0'].values()) if tmp_index!=0 else 0

    # # transition['I0']['D1']
    # # transition['I0']['M1']

    # for i in xrange(len(alignment[0])):
    #     if i not in insert_index:
    #         state_index += 1
    #         transition['I'+str(state_index)] = {}
    #         transition['I'+str(state_index)]['D'+str(state_index+1)] = 0
    #         transition['I'+str(state_index)]['M'+str(state_index+1)] = 0
    #         emission['M'+str(state_index+1)] = dict((x,0) for x in alphabet)

    #         for m in xrange(len(alignment)):
    #             if alignment[m][i] == '-':
    #                 transition['I'+str(state_index)]['D'+str(state_index+1)] += 1
    #             else:
    #                 transition['I'+str(state_index)]['M'+str(state_index+1)] += 1
    #                 emission['M'+str(state_index+1)][alignment[m][i]] += 1


    #         if state_index > 0:
    #             transition['M'+str(state_index)]['I'+str(state_index)] = 0
    #             transition['D'+str(state_index)]['I'+str(state_index)] = 0
    #             emission['I'+str(state_index)] = dict((x,0) for x in alphabet)
    #             for m in xrange(len(alignment)):
    #                 if i+1 not in insert_index and alignment[m][i]



def profile_hmm_pseudocounts(thresh, pseu, alphabet, alignment):

    ##### first label all states, then cal
    thresh = thresh * len(alignment)
    states = []
    insert_index = []
    for i in xrange(len(alignment[0])):
        total = 0
        for j in alignment:
            if j[i] == '-':
                total += 1
        if total >= thresh:
            insert_index.append(i)

    emission = {}
    emission['S'] = dict((x,0) for x in alphabet)
    emission['E'] = dict((x,0) for x in alphabet)
    emission['I0'] = dict((x,0) for x in alphabet)
    for i in xrange(1,len(alignment[0])-len(insert_index)+1):
        emission['I'+str(i)] = dict((x,0) for x in alphabet)
        emission['M'+str(i)] = dict((x,0) for x in alphabet)
        emission['D'+str(i)] = dict((x,0) for x in alphabet)

    for i in xrange(len(alignment)):
        per_state = []
        current_index = 1
        for j in xrange(len(alignment[i])):
            if j not in insert_index:
                if alignment[i][j] == '-':
                    per_state.append('D'+str(current_index))
                else:
                    per_state.append('M'+str(current_index))
                    emission['M'+str(current_index)][alignment[i][j]] += 1
                current_index += 1
            else:
                if alignment[i][j]!='-':
                    per_state.append('I'+str(current_index-1))
                    emission['I'+str(current_index-1)][alignment[i][j]] += 1
        states.append(per_state)

    for key in emission:
        if key!='S' and key!='E' and not key.startswith('D'):
            total = 0
            for sub_key in emission[key]:
                total += emission[key][sub_key]
            if total > 0:
                sub_total = 0
                for sub_key in emission[key]:
                    emission[key][sub_key] = (1.0*emission[key][sub_key])/total+pseu
                    # emission[key][sub_key] = (emission[key][sub_key]+pseu)/(1+pseu*len(emission[key]))
                    # emission[key][sub_key] = (emission[key][sub_key]+pseu)/(1+pseu*len(alphabet))
                    sub_total +=  1.0*emission[key][sub_key]
                for sub_key in emission[key]:
                    emission[key][sub_key] =  emission[key][sub_key]/sub_total


            else:
                for sub_key in emission[key]:
                    emission[key][sub_key] = 1.0/len(alphabet)
    transition = {}
    transition['S']={}
    transition['S']['I0'] = 0
    transition['S']['D1'] = 0
    transition['S']['M1'] = 0
    for i in states:
        transition['S'][i[0]] += 1
    transition['I0']={}
    transition['I0']['I0'] = 0
    transition['I0']['D1'] = 0
    transition['I0']['M1'] = 0
    # for i in states:
    #     transition['I0'][i[0]] += 1

    for i in xrange(len(states)):
        for j in xrange(len(states[i])-1):
            if states[i][j] not in transition:
                transition[states[i][j]] = {}
            if states[i][j+1] not in transition[states[i][j]]:
                transition[states[i][j]][states[i][j+1]] = 0
            transition[states[i][j]][states[i][j+1]] += 1
        if not states[i][len(states[i])-1] in transition:
            transition[states[i][len(states[i])-1]] = {}
        if not 'E' in transition[states[i][len(states[i])-1]]:
            transition[states[i][len(states[i])-1]]['E'] = 0
        transition[states[i][len(states[i])-1]]['E'] += 1

    if 'I'+str(len(alignment[0])-len(insert_index)) not in transition:
        transition['I'+str(len(alignment[0])-len(insert_index))] = {}
        if not 'E' in transition['I'+str(len(alignment[0])-len(insert_index))]:
            transition['I'+str(len(alignment[0])-len(insert_index))]['E'] = 0

    if 'D'+str(len(alignment[0])-len(insert_index)) not in transition:
        transition['D'+str(len(alignment[0])-len(insert_index))] = {}
        if not 'E' in transition['D'+str(len(alignment[0])-len(insert_index))]:
            transition['D'+str(len(alignment[0])-len(insert_index))]['E'] = 0

    if 'M'+str(len(alignment[0])-len(insert_index)) not in transition:
        transition['M'+str(len(alignment[0])-len(insert_index))] = {}
        if not 'E' in transition['M'+str(len(alignment[0])-len(insert_index))]:
            transition['M'+str(len(alignment[0])-len(insert_index))]['E'] = 0

    for i in xrange(1,len(alignment[0])-len(insert_index)+1):
        if not 'I'+str(i) in transition:
            transition['I'+str(i)] = {}
        if not 'M'+str(i) in transition:
            transition['M'+str(i)] = {}
        if not 'D'+str(i) in transition:
            transition['D'+str(i)] = {}

    for key in transition:
        if key!='E':
            total = 0
            for sub_key in transition[key]:
                total += transition[key][sub_key]
            if key!='S' and key!='I0':
                if key[1:]!=str(len(alignment[0])-len(insert_index)):
                    if not 'I'+key[1:] in transition[key]:
                        transition[key]['I'+key[1:]] = 0
                    if not 'D'+str(int(key[1:])+1) in transition[key]:
                        transition[key]['D'+str(int(key[1:])+1)] = 0
                    if not 'M'+str(int(key[1:])+1) in transition[key]:
                        transition[key]['M'+str(int(key[1:])+1)] = 0
                else:
                    if not 'I'+key[1:] in transition[key]:
                        transition[key]['I'+key[1:]] = 0
                    if not 'E' in transition[key]:
                        transition[key]['E'] = 0

            for sub_key in transition[key]:
                if total > 0:
                    transition[key][sub_key] = 1.0*transition[key][sub_key]/total
                    transition[key][sub_key] = (transition[key][sub_key]+pseu)/(1+pseu*len(transition[key]))
                else:
                    if len(transition[key])==3:
                        transition[key][sub_key] = 1.0/3
                    if len(transition[key])==2:
                        transition[key][sub_key] = 1.0/2

    return transition, emission
    # ##### PRINT transition table
    # index_list = ['S', 'I0']
    # for i in xrange(1,len(alignment[0])-len(insert_index)+1):
    #     index_list.extend(['M'+str(i), 'D'+str(i), 'I'+str(i)])
    # index_list.append('E')
    # print ' ',
    # for i in index_list:
    #     print i,
    # print
    # for i in index_list:
    #     print i,
    #     if i in transition:
    #         for j in index_list:
    #             if j in transition[i]:
    #                 print round(transition[i][j],3),
    #             else:
    #                 print 0,
    #         print
    #     else:
    #         for j in index_list:
    #             print 0,
    #         print

    # print '--------'


    # ##### print emission table
    # print ' ',
    # for i in alphabet:
    #     print i,
    # print
    # print 'S',
    # for i in alphabet:
    #     print round(emission['S'][i],3),
    # print
    # print 'I0',
    # for j in alphabet:
    #     print round(emission['I0'][j],3),
    # print

    # # print ' '.join([str(x) for x in dict(sorted(emission['I0'].items())).values()])
    # for i in xrange(1,len(alignment[0])-len(insert_index)+1):

    #     print 'M'+str(i),
    #     for j in alphabet:
    #         print round(emission['M'+str(i)][j],3),
    #     print

    #     print 'D'+str(i),
    #     for j in alphabet:
    #         print round(emission['D'+str(i)][j],3),
    #     print
    #     print 'I'+str(i),
    #     for j in alphabet:
    #         print round(emission['I'+str(i)][j],3),
    #     print



    # print 'E',
    # for j in alphabet:
    #     print round(emission['E'][j],3),
    # print










def likelihood(string, states, transition, emission):
    p = 1
    dic = {}

    dic[0] = {}
    for i in states:
        dic[0][i] = {}
        dic[0][i] = 1.0/len(states)*emission[(i,string[0])]
    for i in xrange(1,len(string)):
        dic[i] = {}
        for j in states:
            dic[i][j] = 0
            for k in states:
                dic[i][j] += dic[i-1][k]*transition[(k, j)]*emission[(j,string[i])]
    res = 0
    for i in states:
        res += dic[len(string)-1][i]
    return res


def soft_decoding(string, states, transition, emission):
    forward = {}
    forward[0] = {}
    for i in states:
        forward[0][i] = {}
        forward[0][i] = 1.0/len(states)*emission[i][string[0]]
    for i in xrange(1,len(string)):
        forward[i] = {}
        for j in states:
            forward[i][j] = 0
            for k in states:
                forward[i][j] += forward[i-1][k]*transition[k][j]*emission[j][string[i]]

    backward = {}
    backward[len(string)-1] = {}
    for i in states:
        backward[len(string)-1][i] = {}
        backward[len(string)-1][i] = 1.0 ###*emission[i][re_string[0]]
    for i in range(len(string)-2, -1,-1):
        backward[i] = {}
        for j in states:
            backward[i][j] = 0
            for k in states:
                backward[i][j] += backward[i+1][k]*transition[j][k]*emission[k][string[i+1]]
    res = {}
    for i in xrange(len(string)):
        res[i] = {}
        total = 0
        for j in states:
            res[i][j] = forward[i][j]*backward[i][j]
            total +=  res[i][j]
        for j in states:
            res[i][j] = res[i][j]/total

    return res




def seq_align(string, thresh, pseu, alphabet, alignment):
    transition, emission = profile_hmm_pseudocounts(thresh, pseu, alphabet, alignment)
    rows = len(emission)/3-1

    index_list = ['S', 'I0']
    for i in xrange(0,rows):
        index_list.extend(['M'+str(i), 'D'+str(i), 'I'+str(i)])
    index_list.append('E')
    for i in index_list:
        if not i in transition:
            transition[i] = {}
        for j in index_list:
            if not j in transition[i]:
                transition[i][j] = 0

    M = [[0 for i in xrange(len(string)+1)] for i in xrange(rows+1)]
    I = [[0 for i in xrange(len(string)+1)] for i in xrange(rows+1)]
    D = [[0 for i in xrange(len(string)+1)] for i in xrange(rows+1)]

    for i in xrange(1,len(string)+1):
        if i == 1:
            I[0][i] = max(transition['S']['I0']*emission['I0'][string[i-1]],
                          transition['S']['I0']*emission['I0'][string[i-1]],
                          transition['S']['I0']*emission['I0'][string[i-1]])
        else:
            I[0][i] = max(I[0][i-1]*transition['I0']['I0']*emission['I0'][string[i-1]],
                          I[0][i-1]*transition['I0']['I0']*emission['I0'][string[i-1]],
                          I[0][i-1]*transition['I0']['I0']*emission['I0'][string[i-1]])

    for i in xrange(1,rows+1):
        if i==1:
            D[i][0] = transition['S']['D'+str(i)]
        else:
            D[i][0] = D[i-1][0]*transition['D'+str(i-1)]['D'+str(i)]




    for j in xrange(1,rows+1):
        for i in xrange(1,len(string)+1):
            if j-1==0 and i == 1:
                M[j][i] = max(transition['S']['M1']*emission['M'+str(j)][string[i-1]],
                              transition['S']['M1']*emission['M'+str(j)][string[i-1]],
                              transition['S']['M1']*emission['M'+str(j)][string[i-1]])
                D[j][i] = I[j-1][i]*transition['I'+str(j-1)]['D'+str(j)]
                I[j][i] = max(D[j][i-1]*transition['D'+str(j)]['I'+str(j)]*emission['I'+str(j)][string[i-1]],
                              M[j][i-1]*transition['M'+str(j)]['I'+str(j)]*emission['I'+str(j)][string[i-1]],
                              I[j][i-1]*transition['I'+str(j)]['I'+str(j)]*emission['I'+str(j)][string[i-1]])

                # else:
                #     M[j][i] = max(I[j-1][i-1]*transition['S']['M1']*emission['M'+str(j)][string[i-1]],
                #                   D[j-1][i-1]*transition['S']['M1']*emission['M'+str(j)][string[i-1]],
                #                   M[j-1][i-1]*transition['S']['M1']*emission['M'+str(j)][string[i-1]])
                #     D[j][i] = max(M[j-1][i]*transition['S']['D1'],
                #                   I[j-1][i]*transition['S']['D1'],
                #                   D[j-1][i]*transition['S']['D1'])

            else:
                M[j][i] = max(I[j-1][i-1]*transition['I'+str(j-1)]['M'+str(j)]*emission['M'+str(j)][string[i-1]],
                              D[j-1][i-1]*transition['D'+str(j-1)]['M'+str(j)]*emission['M'+str(j)][string[i-1]],
                              M[j-1][i-1]*transition['M'+str(j-1)]['M'+str(j)]*emission['M'+str(j)][string[i-1]])
                D[j][i] = max(M[j-1][i]*transition['M'+str(j-1)]['D'+str(j)],
                              I[j-1][i]*transition['I'+str(j-1)]['D'+str(j)],
                              D[j-1][i]*transition['D'+str(j-1)]['D'+str(j)])
                I[j][i] = max(D[j][i-1]*transition['D'+str(j)]['I'+str(j)]*emission['I'+str(j)][string[i-1]],
                              M[j][i-1]*transition['M'+str(j)]['I'+str(j)]*emission['I'+str(j)][string[i-1]],
                              I[j][i-1]*transition['I'+str(j)]['I'+str(j)]*emission['I'+str(j)][string[i-1]])


    #####  retrieve the mappping sequences
    res = []
    state = rows
    seq = len(string)
    max_value = 0
    max_state = ('', 0, 0)
    next_state = 'E'
    while seq>0:
        if I[state][seq] > max_value:
            max_value =  I[state][seq]*transition['I'+str(state)][next_state]
            max_state = ('I', state, seq)
        if M[state][seq] > max_value:
            max_value =  M[state][seq]*transition['M'+str(state)][next_state]
            max_state = ('M', state, seq)
        if D[state][seq] > max_value:
            max_value =  D[state][seq]*transition['D'+str(state)][next_state]
            max_state = ('D', state, seq)

        res.insert(0,max_state[0]+str(max_state[1]))
        next_state = res[0]
        if max_state[0] == 'I':
            seq -= 1
        if max_state[0] == 'D':
            state -= 1
        if max_state[0] == 'M':
            seq -= 1
            state -= 1
    return res


def parameter_estimation(string, alphabet, path, states):
    transition = {}
    for i in states:
         transition[i] = dict((x,0) for x in states)
    emission = {}
    for i in states:
         emission[i] = dict((x,0) for x in alphabet)
    for i in xrange(len(path)):
        if i+1<len(path):
            transition[path[i]][path[i+1]] += 1
        emission[path[i]][string[i]] += 1

    for i in transition:
        total = sum(transition[i].values())
        for j in transition[i]:
            if total>0:
                transition[i][j] = 1.0* transition[i][j]/total
            else:
                transition[i][j] = 1.0/len(states)

    for i in emission:
        total = sum(emission[i].values())
        for j in emission[i]:
            if total >0:
                emission[i][j] = 1.0*emission[i][j]/total
            else:
                emission[i][j] = 1.0/len(alphabet)

    return transition, emission



if __name__ == '__main__':

    # f = open('test', 'r')
    # lines = f.readlines()
    # path = lines[0].strip()
    # states = lines[2].strip().split()
    # transition = {}
    # for i in xrange(5,5+len(states)):
    #     items = lines[i].strip().split()
    #     for j in xrange(1,len(items)):
    #         transition[(states[i-5], states[j-1])] = float(items[j])
    # res = prob(path, transition)
    # print res


    # f = open('test', 'r')
    # lines = f.readlines()
    # string = lines[0].strip()
    # alphabet = lines[2].strip().split()
    # path = lines[4].strip()
    # states = lines[6].strip().split()
    # emission = {}
    # for i in xrange(9,9+len(states)):
    #     items = lines[i].strip().split()
    #     for j in xrange(1,len(items)):
    #         emission[(states[i-9], alphabet[j-1])] = float(items[j])
    # res = emitt_prob(string, path, emission)
    # print res


    # f = open('test', 'r')
    # lines = f.readlines()
    # string = lines[0].strip()
    # alphabet = lines[2].strip().split()
    # states = lines[4].strip().split()
    # transition = {}
    # for i in xrange(7,7+len(states)):
    #     items = lines[i].strip().split()
    #     for j in xrange(1,len(items)):
    #         transition[(states[i-7], states[j-1])] = float(items[j])

    # emission = {}
    # for i in xrange(11,11+len(states)):
    #     items = lines[i].strip().split()
    #     for j in xrange(1,len(items)):
    #         emission[(states[i-11], alphabet[j-1])] = float(items[j])


    # # res = decoding(string, states, transition, emission)
    # res = likelihood(string, states, transition, emission)
    # print res




    # f = open('test', 'r')
    # lines = f.readlines()
    # thresh  = float(lines[0].strip())
    # alphabet = lines[2].strip().split()
    # alignment = []
    # for i in xrange(4,len(lines)):
    #     alignment.append(lines[i].strip())


    # profile_hmm(thresh, alphabet, alignment)



    # f = open('test', 'r')
    # lines = f.readlines()
    # thresh  = float(lines[0].strip().split()[0])
    # pseu  = float(lines[0].strip().split()[1])

    # alphabet = lines[2].strip().split()
    # alignment = []
    # for i in xrange(4,len(lines)):
    #     alignment.append(lines[i].strip())


    # profile_hmm_pseudocounts(thresh, pseu, alphabet, alignment)


    # f = open('test', 'r')
    # lines = f.readlines()
    # string = lines[0].strip()
    # thresh  = float(lines[2].strip().split()[0])
    # pseu  = float(lines[2].strip().split()[1])

    # alphabet = lines[4].strip().split()
    # alignment = []
    # for i in xrange(6,len(lines)):
    #     alignment.append(lines[i].strip())


    # print ' '.join(seq_align(string, thresh, pseu, alphabet, alignment))

    # f = open('test', 'r')
    # lines = f.readlines()
    # string = lines[0].strip()
    # alphabet = lines[2].strip().split()
    # path = lines[4].strip()
    # states = lines[6].strip().split()
    # transition, emission = parameter_estimation(string, alphabet, path, states)
    # print '  ',
    # print ' '.join(states)
    # for i in states:
    #     print i,
    #     for j in states:
    #         print transition[i][j],
    #     print

    # print '--------'
    # print '  ',
    # print ' '.join(alphabet)
    # for i in states:
    #     print i,
    #     for j in alphabet:
    #         print emission[i][j],
    #     print



    # ##### Viterbi learning
    # f = open('test', 'r')
    # lines = f.readlines()
    # num = int(lines[0])
    # string = lines[2].strip()
    # alphabet = lines[4].strip().split()
    # states = lines[6].strip().split()

    # transition = {}
    # for i in states:
    #     transition[i] = dict((x,0) for x in states)
    # emission = {}
    # for i in states:
    #      emission[i] = dict((x,0) for x in alphabet)

    # for i in xrange(9,9+len(states)):
    #     items = lines[i].strip().split()
    #     for j in xrange(1,len(items)):
    #         transition[states[i-9]][states[j-1]] = float(items[j])


    # for i in xrange(13,13+len(states)):
    #     items = lines[i].strip().split()
    #     for j in xrange(1,len(items)):
    #         emission[states[i-13]][alphabet[j-1]] = float(items[j])

    # ac_num = 1
    # while ac_num<=num:
    #     path = decoding(string, states, transition, emission)
    #     transition, emission = parameter_estimation(string, alphabet, path, states)
    #     ac_num += 1

    # print '  ',
    # print ' '.join(states)
    # for i in states:
    #     print i,
    #     for j in states:
    #         print transition[i][j],
    #     print

    # print '--------'
    # print '  ',
    # print ' '.join(alphabet)
    # for i in states:
    #     print i,
    #     for j in alphabet:
    #         print emission[i][j],
    #     print


    #####
    f = open('test', 'r')
    lines = f.readlines()
    string = lines[0].strip()
    alphabet = lines[2].strip().split()
    states = lines[4].strip().split()
    transition = {}
    for i in states:
        transition[i] = dict((x,0) for x in states)
    emission = {}
    for i in states:
         emission[i] = dict((x,0) for x in alphabet)


    for i in xrange(7,7+len(states)):
        items = lines[i].strip().split()
        for j in xrange(1,len(items)):
            transition[states[i-7]][states[j-1]] = float(items[j])

    for i in xrange(9+len(states),9+2*len(states)):
        items = lines[i].strip().split()
        for j in xrange(1,len(items)):
            emission[states[i-9-len(states)]][alphabet[j-1]] = float(items[j])


    res = soft_decoding(string, states, transition, emission)
    for i in states:
        print i,
    print
    for i in xrange(len(string)):
        for j in states:
            print res[i][j],
        print
