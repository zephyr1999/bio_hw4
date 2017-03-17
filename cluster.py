from platform import node
import collections

It = collections.Iterable



def flatten(L):
    for e in L:
        if isinstance(e, It) and not isinstance(e, basestring):
            for sub in flatten(e):
                yield sub
        else:
            yield e

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

def one_round(list_of_possible_cluster_pairs, dictionary_of_seq_compare_scores, node_dict):
    # create list of tuples of all possible clusters with distance by calling dictionary with clusters
    list_of_possible_cluster_pairs_with_distances = [(dictionary_of_seq_compare_scores[cluster],cluster) for cluster in list_of_possible_cluster_pairs]
    
    #sort list of possible cluster with distances and pull out lowest one
    lowest_distance, smallest_distance_cluster = sorted(list_of_possible_cluster_pairs_with_distances)[0]
    
    listlistlist.append(lowest_distance)

    save_node_data(smallest_distance_cluster, lowest_distance , node_dict)
    
    # create new list that replaced the seqs that were clustered as one
    new_list_of_possible_cluster_pairs = sorted(collapse(list_of_possible_cluster_pairs, smallest_distance_cluster))


    # update dictionary with the new cluster and calculate the new distance between other possible clusters
    for possible_clusters in new_list_of_possible_cluster_pairs:
        if possible_clusters not in dictionary_of_seq_compare_scores:
            dictionary_of_seq_compare_scores[possible_clusters] = average_distance(possible_clusters,dictionary_of_seq_compare_scores)
 
    return new_list_of_possible_cluster_pairs
    

def UPGMA(dictionary_of_seq_compare_scores, list_of_compared_seqs):

    node_dict = dict()

    while list_of_compared_seqs:
        list_of_compared_seqs = one_round(list_of_compared_seqs, dictionary_of_seq_compare_scores, node_dict)
        print 'list_of_compared_seqs', list_of_compared_seqs
    
    return node_dict   


    '''
def UPGMA(dictionary_of_seq_compare_scores, list_of_compared_seqs):
    
    node_dict = run(dictionary_of_seq_compare_scores, list_of_compared_seqs)
    
    return node_dict
   '''
    '''   
    print listlistlist[0][0] + listlistlist[0][1] + "=" + "(" + listlistlist[0][0] + ":" + str(node_dict[listlistlist[0][0]]['up']) + ','+ listlistlist[0][1] + ":" + str(node_dict[listlistlist[0][1]]['up']) + ")"
    print listlistlist[0][1] + listlistlist[0][0] + "=" + "(" + listlistlist[0][0] + ":" + str(node_dict[listlistlist[0][0]]['up']) + ','+ listlistlist[0][1] + ":" + str(node_dict[listlistlist[0][1]]['up']) + ")"
    
    print listlistlist[1][1] + listlistlist[1][0] + "=" + "(" + listlistlist[1][0] + ":" + str(node_dict[listlistlist[1][0]]['up']) + ','+ listlistlist[1][1] + ":" + str(node_dict[listlistlist[1][1]]['up']) + ")"
    print listlistlist[1][0] + listlistlist[1][1] + "=" + "(" + listlistlist[1][0] + ":" + str(node_dict[listlistlist[1][0]]['up']) + ','+ listlistlist[1][1] + ":" + str(node_dict[listlistlist[1][1]]['up']) + ")"
    

    print listlistlist[2][0] + listlistlist[2][1] + "=" + "(" + listlistlist[2][0] + ":" + str(node_dict[listlistlist[2][0]]['up']) + ','+ listlistlist[2][1] + ":" + str(node_dict[listlistlist[2][1]]['up']) + ")"
    print listlistlist[2][1] + listlistlist[2][0] + "=" + "(" + listlistlist[2][0] + ":" + str(node_dict[listlistlist[2][0]]['up']) + ','+ listlistlist[2][1] + ":" + str(node_dict[listlistlist[2][1]]['up']) + ")"
    

    
    print listlistlist[3][1] + listlistlist[3][0] + "=" + "(" + listlistlist[3][0] + ":" + str(node_dict[listlistlist[3][0]]['up']) + ','+ listlistlist[3][1] + ":" + str(node_dict[listlistlist[3][1]]['up']) + ")"
    print listlistlist[3][0] + listlistlist[3][1] + "=" + "(" + listlistlist[3][0] + ":" + str(node_dict[listlistlist[3][0]]['up']) + ','+ listlistlist[3][1] + ":" + str(node_dict[listlistlist[3][1]]['up']) + ")"
    '''
    
    
    
    
    
    
    
    
    
     
     
     
     
     
     
     
     
     
     
     