from platform import node


def new_distance(possible_clusters, dictionary_of_seq_compare_scores):
    
    list_of_distances = []
    
    left = (sorted(list(possible_clusters[0])))
    right = (sorted(list(possible_clusters[1])))

    for seq_1 in left:
        for seq_2 in right:
            distance = dictionary_of_seq_compare_scores[(seq_1,seq_2)]

            list_of_distances.append(distance)
    #Benny add up all the labels to caoolapse and divide by number of adds
    new_distance = sum(list_of_distances)*1.0/len(list_of_distances)
    return new_distance


def update_possible_clusters(list_of_possible_cluster_pairs, smallest_distance_cluster):
    
    #turn tuple into list and smash together
    node = ''.join(((list(smallest_distance_cluster))))
    
    new_list_of_possible_cluster_pairs = list()
    for possible_cluster_tuple in list_of_possible_cluster_pairs:

        left,right = possible_cluster_tuple
        for tip in left:
            if tip in node:
                left = node
        for tip in right:
            if tip in node:
                right = node
        if not left == right:
            new_list_of_possible_cluster_pairs.append((left,right))
    new_list_of_possible_cluster_pairs = sorted(list(set(new_list_of_possible_cluster_pairs)))


    return new_list_of_possible_cluster_pairs


def build_dict_tree(smallest_distance_cluster_tuple, lowest_distance, node_dict):
    #smallest_distance_cluster, lowest_distance , node_dict
    # join items like (('A','B'),'C') into 'ABC'
    #labels = []
    left = ''.join((sorted(list(smallest_distance_cluster_tuple[0]))))
    right =  ''.join((sorted(list(smallest_distance_cluster_tuple[1]))))
    new_node = ''.join((sorted(list(left+right))))
    lowest_distance *= 0.5
    node_dict[new_node] = { 'left_child':left, 'right_child':right, 'dis_to_base':lowest_distance }

    
    #update dict_node with nodes creating parents and children
    #print new_node, node_dict[new_node]
    for i,child_node in enumerate([left,right]):
        if child_node not in node_dict:
            node_dict[child_node] =  {'parent':new_node, 'dis_to_par':lowest_distance }
        else:
            up_distance = lowest_distance - node_dict[child_node]['dis_to_base']
            node_dict[child_node].update({ 'parent':new_node, 'dis_to_par':up_distance} )


def find_smallest_distance(list_of_possible_cluster_pairs, dictionary_of_seq_compare_scores, node_dict):
    # create list of tuples of all possible clusters with distance by calling dictionary with clusters
    list_of_possible_cluster_pairs_with_distances = [(dictionary_of_seq_compare_scores[cluster],cluster) for cluster in list_of_possible_cluster_pairs]
    
    #sort list of possible cluster with distances and pull out lowest one
    lowest_distance, smallest_distance_cluster = sorted(list_of_possible_cluster_pairs_with_distances)[0]
    
    #build_dict_tree
    build_dict_tree(smallest_distance_cluster, lowest_distance , node_dict)
    
    # create new list that replaced the seqs that were clustered as one
    new_list_of_possible_cluster_pairs = sorted(update_possible_clusters(list_of_possible_cluster_pairs, smallest_distance_cluster))


    # update dictionary with the new cluster and calculate the new distance between other possible clusters
    for possible_clusters in new_list_of_possible_cluster_pairs:
        if possible_clusters not in dictionary_of_seq_compare_scores:
            dictionary_of_seq_compare_scores[possible_clusters] = new_distance(possible_clusters,dictionary_of_seq_compare_scores)
 
    return new_list_of_possible_cluster_pairs
    

def UPGMA(dictionary_of_seq_compare_scores, list_of_compared_seqs):

    node_dict = dict()

    while list_of_compared_seqs:
        list_of_compared_seqs = find_smallest_distance(list_of_compared_seqs, dictionary_of_seq_compare_scores, node_dict)
   
    
    return node_dict   
    
    
    
    
    
    
    
     
     
     
     
     
     
     
     
     
     
     