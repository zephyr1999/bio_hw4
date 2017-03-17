#import utils
from platform import node

import collections
It = collections.Iterable

'''
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
'''

'''
def load_data(fn,do_split=False):
    FH = open(fn,'r')
    data = FH.read().strip()
    FH.close()
    if do_split:
        return data.split('\n')
    return data
'''

def flatten(L):
    for e in L:
        if isinstance(e, It) and not isinstance(e, basestring):
            for sub in flatten(e):
                yield sub
        else:
            yield e

'''
def print_list(L, n=3):
    while L:
        for e in L[:n]:
            print 'dsfjaskfhnljkasfhldjsasfkjsalfdjskahjklf', e,
            print
            L = L[n:]
            '''

def list_elements(t, sort_them=True):
    return sorted(list(flatten(t)))

listlistlist = list()

def average_distance(tuple_to_find_new_average,D,debug=False):

    #Benny new list
    dL = list()
    
    t0 = list_elements(tuple_to_find_new_average[0])
    t1 = list_elements(tuple_to_find_new_average[1])

    for label_1 in t0:
        for label_2 in t1:
            d = D[(label_1,label_2)]
            #if debug:
            #    print u+v, d,
            dL.append(d)
    #Benny add up all the labels to caoolapse and divide by number of adds
    average = sum(dL)*1.0/len(dL)
    return average

# replace elements of t with new node
def collapse(L,node_in,debug=False):
    node = ''.join(list_elements(node_in))
    #if debug:
    #    print 'node', node
    #    print 'L'
     #   node, utils.print_list(L, n=4)
    rL = list()
    for item in L:
        left,right = item
        if debug:
            print 'left', left, 'right', right
        for tip in left:
            if tip in node:
                left = node
        for tip in right:
            if tip in node:
                right = node
        if not left == right:
            rL.append((left,right))
    rL = sorted(list(set(rL)))
    #if debug:
    #    print 'rL after set:'
    #    utils.print_list(rL)
    return rL
#-----------------------------------------------
def save_node_data(t,d,node_dict,debug=False):
    # join items like (('A','B'),'C') into 'ABC'
    labels = []
    left = ''.join(list_elements(t[0]))
    right =  ''.join(list_elements(t[1]))
    new_node = ''.join(list_elements(left+right))
    d *= 0.5
    node_dict[new_node] = { 'left':left, 'right':right, 'to_tips':d }
    #if debug:
    print 'new node:'
    print new_node, node_dict[new_node]
    for i,child_node in enumerate([left,right]):
        if not child_node in node_dict:
            node_dict[child_node] =  {'parent':new_node, 'up':d }
        else:
            up_d = d - node_dict[child_node]['to_tips']
            node_dict[child_node].update({ 'parent':new_node, 'up':up_d} )
     #   if debug:
    #        print ['left node:','right_node:'][i]
     #       print child_node, node_dict[child_node]
    #labels[a] = "(" + labels[0] + "," + labels[1] + ")"
    #print str(node_dict['left'])
    #print 'testestest', labels[0]

def one_round(L,D,node_dict,debug=False):
    # find the pair of nodes with the smallest distance
    temp = [(D[k],k) for k in L]
    
    print 'temp', temp
    lowest_labels,lowest_distance = sorted(temp)[0]
    #print 'lowest labels' , lowest_distance
    listlistlist.append(lowest_distance)
    #if debug:
    #    print 'closest:'
    #print lowest_distance, lowest_distance
    save_node_data(lowest_distance,lowest_labels,node_dict,debug=debug)
    # collapse the list
    rL = sorted(collapse(L,lowest_distance))
    #if debug:
    #    print 'elements after joining:'
    #    utils.print_list(rL,n=1)
    # calculate cluster distances
    for lowest_distance in rL:
        if not lowest_distance in D:
            D[lowest_distance] = average_distance(lowest_distance,D,debug=debug)
    #print 'stuff', rL, t
    #print D
    return rL,lowest_distance
    

#def run(fn,debug=False):
    #D,L = get_data_dict(fn,debug=debug)
def run(D,L, debug= False):
    print 'DDDDDDDDDDDD',D
    

    #D = {('B', 'A'): 17.0, ('D', 'E'): 43.0, ('C', 'D'): 28.0, ('A', 'B'): 17.0, ('E', 'A'): 23.0, ('B', 'B'): 0.0, ('E', 'E'): 0.0, ('D', 'A'): 31.0, ('C', 'C'): 0.0, ('D', 'B'): 34.0, ('B', 'C'): 30.0, ('A', 'A'): 0.0, ('E', 'D'): 43.0, ('A', 'E'): 23.0, ('A', 'D'): 31.0, ('E', 'C'): 39.0, ('B', 'D'): 34.0, ('D', 'D'): 0.0, ('B', 'E'): 21.0, ('A', 'C'): 21.0, ('C', 'A'): 21.0, ('E', 'B'): 21.0, ('C', 'B'): 30.0, ('D', 'C'): 28.0, ('C', 'E'): 39.0}
    #print D
    print  L
    #L = [('B', 'A'), ('C', 'A'), ('C', 'B'), ('D', 'A'), ('D', 'B'), ('D', 'C'), ('E', 'A'), ('E', 'B'), ('E', 'C'), ('E', 'D')]
    print L
    #Benny create an empty dict
    node_dict = dict()
  
    counter = 0
    while L:
        counter += 1
        #if debug:
        #    print '\nround', counter
        L,t = one_round(L,D,node_dict,debug=debug)
        print 'L', L, 't', t  
    
    #if debug:
    #    print t, '\n'
    #    for k in node_dict:
    #        print k, node_dict[k]
    return node_dict   

def join_labels(labels):
   
    #print 'nummmmmmmm', num
    # Join the labels in the first index
    labels[a] = "(" + labels[a] + "," + labels[b] + ':'")"
    #print labels
    # Remove the (now redundant) label in the second index
    del labels[b]


    # Return the x, y co-ordinate of cell
    return x, y

#-----------------------------------------------
if __name__ == '__main__':
    #fn = 'upgma_data.txt'
    #fn = 'upgma_Sarich_data.txt'
    node_dict = run(fn,debug=True)
    

    
    print '***'
    def f(k):  return len(k)
    
    L = sorted(node_dict.keys(),key=f)
    print "lllllllll", L
    for k in L[0:]:
        print k,
    print
    print node_dict
    print 'please', listlistlist
    
   # for i in listlistlist:
        #x = join_labels(i)
    #    print 'xxx', x
        
    print listlistlist[0][0] + listlistlist[0][1] + "=" + "(" + listlistlist[0][0] + ":" + str(node_dict[listlistlist[0][0]]['up']) + ','+ listlistlist[0][1] + ":" + str(node_dict[listlistlist[0][1]]['up']) + ")"
    print listlistlist[0][1] + listlistlist[0][0] + "=" + "(" + listlistlist[0][0] + ":" + str(node_dict[listlistlist[0][0]]['up']) + ','+ listlistlist[0][1] + ":" + str(node_dict[listlistlist[0][1]]['up']) + ")"
    
    print listlistlist[1][1] + listlistlist[1][0] + "=" + "(" + listlistlist[1][0] + ":" + str(node_dict[listlistlist[1][0]]['up']) + ','+ listlistlist[1][1] + ":" + str(node_dict[listlistlist[1][1]]['up']) + ")"
    print listlistlist[1][0] + listlistlist[1][1] + "=" + "(" + listlistlist[1][0] + ":" + str(node_dict[listlistlist[1][0]]['up']) + ','+ listlistlist[1][1] + ":" + str(node_dict[listlistlist[1][1]]['up']) + ")"
    

    print listlistlist[2][0] + listlistlist[2][1] + "=" + "(" + listlistlist[2][0] + ":" + str(node_dict[listlistlist[2][0]]['up']) + ','+ listlistlist[2][1] + ":" + str(node_dict[listlistlist[2][1]]['up']) + ")"
    print listlistlist[2][1] + listlistlist[2][0] + "=" + "(" + listlistlist[2][0] + ":" + str(node_dict[listlistlist[2][0]]['up']) + ','+ listlistlist[2][1] + ":" + str(node_dict[listlistlist[2][1]]['up']) + ")"
    

    
    print listlistlist[3][1] + listlistlist[3][0] + "=" + "(" + listlistlist[3][0] + ":" + str(node_dict[listlistlist[3][0]]['up']) + ','+ listlistlist[3][1] + ":" + str(node_dict[listlistlist[3][1]]['up']) + ")"
    print listlistlist[3][0] + listlistlist[3][1] + "=" + "(" + listlistlist[3][0] + ":" + str(node_dict[listlistlist[3][0]]['up']) + ','+ listlistlist[3][1] + ":" + str(node_dict[listlistlist[3][1]]['up']) + ")"
    
    
    
    
    print node_dict['ABCDE']
    #labels[a] = "(" + labels[a] +  "," + labels[b] +  ")"
    
    
    
    
    
    
    
    
    
     
     
     
     
     
     
     
     
     
     
     