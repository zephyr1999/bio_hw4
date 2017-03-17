# Homework 4
# Erik Holbrook Jorge Benavides Cosima Jackson

################################################################################################################################
#    References:
#    http://stackoverflow.com/questions/8568233/print-float-to-n-decimal-places-including-trailing-0s
#    http://stackoverflow.com/questions/3636344/read-flat-list-into-multidimensional-array-matrix-in-python
#    http://stackoverflow.com/questions/17870612/printing-a-two-dimensional-array-in-python
#        
################################################################################################################################

import argparse
from os import path
import numpy as np  #for dealing with matrix 
from matrix import global_dp_edit
from cluster import UPGMA



################################################################################################################################
#    Usage function to help the user type in the correct command to run the file
################################################################################################################################

def usage():
    
    print '\npython hw4.py -f <filename> -s <filename> -g <negative_number>\n'
    print "where -f is the name of a FATSA format file to be read and analyzed"
    print "where -g is the gap penalty you wish to implement"
    print "where -s is the name of a scoring file to be used in calculating the distance"

################################################################################################################################
#    parse_file function: this function is passed in the file_handler after being opened in a for loop. Sets two varibles to empty
#    seq_name and seq. Then it goes line by line through the file only yielding an answer once it has bott the name and seq. This 
#    is a generator so it doesn't have to go through the entire function before returning answer nor does it have to start at the 
#    beginning of the function on each iteration from the for loop calling it. This saves memory since it doesn't have to create a
#    data structure to return the answer.
################################################################################################################################ 
   
def parse_file(file_handler):
    seq_name = None
    seq =  []
    
    for line in file_handler:
        #strip off \n character and empty space
        line = line.rstrip()
        if line.startswith(">"):
            if seq_name: 
                yield (seq_name, ''.join(seq))
            #On first readline this function fails the if seq_name. writes name to seq_name and then fils in the seq by reading lines
            #up to the next >, loops back enters if '>' and returns seq_name and seq
            seq_name1 = line.split() 
            seq_name = seq_name1[0]
            seq = []
        else:
            seq.append(line.rstrip().replace(" ", ""))
    if seq_name: 
        #Since I skip the first if statement to wait for the seq to get filled in I have to make one last call in order to get
        #the last seq_name and seq
        yield (seq_name, ''.join(seq).upper())
        
################################################################################################################################
#    Main: Handle Passed in Arguments
################################################################################################################################ 

def main():

    #create an instance of argument parser
    parse = argparse.ArgumentParser()
    
    #add arguments to parser so if command line argument matches -f or -F or --filename it will take the next argument
    #and put it into the --filename. See reference for more details on argparse.
    parse.add_argument('-F', '-f', '--filename')
    parse.add_argument('-G', '-g', '--gap')
    parse.add_argument('-S', '-s', '--score_filename')
    
    #create instance of parse_args
    args = parse.parse_args()
    
    #set the args to variable names for easy reference
    filename = args.filename
    gap_penalty = args.gap
    gap_penalty = int(gap_penalty)
    score_filename = args.score_filename
    
    #error handling if any variables are empty something went wrong call usage function to inform user
    if(filename == None):
        usage()
        exit(2)
    
    if(score_filename == None):
        usage()
        exit(2)
        
################################################################################################################################
#    Main: Parse Score file into a dictionary inside dictionary representing the scores
################################################################################################################################       
        
    #get absolute file path for filename and score_filename   
    filepath = path.abspath(filename)
    score_filepath = path.abspath(score_filename)
    
    #parse the score_file
    results = []
    with open(score_filepath) as inputfile:                  # read in scoring matrix file
        for line in inputfile:
            results.append(line.strip('\n ').split(','))

    new_r = reduce(lambda x,y: x+y, [x[0].split('\t') for x in results]) # remove new lines and tabs
    new_r = np.mat(new_r) # make array into 4 x 5 matrix
    new_r = new_r.reshape(4,5)


    keys = new_r[:,0] # column 0 = A,C,G,T
    #turn matrix object into list 
    keys = keys.tolist()
    new_r = new_r.tolist()
    #combine list of list into one list of string ['A','B',....,'D'}
    answer = [item for sublist in keys for item in sublist]
    #print answer

    dict1 = {}
    dict2 = {}

    for i in range(0, len(answer), 1):
        dict2[answer[i]] = {}
        for j in range(0, len(answer), 1):
            dict1[answer[j]] = int(new_r[i][j+1])
            dict2[answer[i]][answer[j]] = dict1[answer[j]]

################################################################################################################################
#    Main: Parse FASTA file into a array_of_seq_names and array_of_seq
################################################################################################################################  
                                        
    #open file and loop through parsing out and returning the sequences
    array_of_seq = []
    array_of_seq_names = []
    with open(filepath) as f:
        for dna_sequence in parse_file(f): #runs in O(n) sinc 
            array_of_seq.append(dna_sequence[1])
            array_of_seq_names.append(dna_sequence[0])

    upper_tri_distance_matrix = []
    
    #loop through list of seq and compare ever seq to eachother. Take the length of the seq returned
    #and divide number of matches by th elength to get a similarity score. Put score in array for each seq in order
    '''
    for i in range(0, len(array_of_seq)):
        row_in_distance_matrix = []
        for j in range(i+1, len(array_of_seq)):
            edit_distance = global_dp_edit(array_of_seq[i], array_of_seq[j], gap_penalty, dict2)
            row_in_distance_matrix.append( edit_distance )
        upper_tri_distance_matrix.append(row_in_distance_matrix)
    
    #reverse distance matrix so it is now in lower form
    lower_tri_distance_matirx = upper_tri_distance_matrix[::-1]
    '''
    
    ############FOR TESTING
    lower_tri_distance_matirx = [[],[17],[21,30],[31,34,28],[23,21,39,43]]
    array_of_seq_names = ['A','B','C','D','E']
    
    #create empty matrix size of # of seqs * # of seqs
    number_of_seqs = len(array_of_seq_names)
    w, h = number_of_seqs, number_of_seqs;
    distance_Matrix = [[0 for x in range(w)] for y in range(h)]
    
    #create full matrix for print by copying lower triangle to upper trangle of newly formed empty distance_matrix
    for i in range(number_of_seqs):
        for j in range(i+1, number_of_seqs):
            distance_Matrix[i][j] = lower_tri_distance_matirx[j][i]
            distance_Matrix[j][i] = distance_Matrix[i][j]
             
    print('\nDistance Matrix')
    print('\n'.join(['\t'.join(['{:<}'.format(item) for item in row]) for row in distance_Matrix]) + '\n')      

    
    dictionary_of_seq_compare_scores = {}
    
    #create dictionary of all seq comparison scroes
    for i in range(0, number_of_seqs, 1):
        for j in range(0, number_of_seqs, 1):  
            xx = (str(array_of_seq_names[i]) , str(array_of_seq_names[j]) )
            dictionary_of_seq_compare_scores[xx] = float(distance_Matrix[i][j])
            
    pos_and_seq = enumerate(array_of_seq_names)
    
    #create list of all seqs only compared to each other once non redundant
    list_of_compared_seqs = [(seq1,seq2) for pos,seq1 in pos_and_seq for seq2 in array_of_seq_names[pos+1:]]     
    #print list_of_compared_seqs
    #
    node_dict, list_of_smallest_clusters = UPGMA(dictionary_of_seq_compare_scores, list_of_compared_seqs)
    

    print node_dict, '\n'
    #listlist = listlist[::-1]
    print list_of_smallest_clusters
    count = 1
    answer= ['']

    for smallest_distance_cluster in list_of_smallest_clusters:
    
        
        left_tuple = str(smallest_distance_cluster[0])
        right_tuple = str(smallest_distance_cluster[1])
        print left_tuple
    
        if count == 1:
            #answer[0] = answer[0] + left_tuple
            if left_tuple not in answer[0] and right_tuple not in answer[0]:
                answer[0] = "(" + left_tuple + "," + right_tuple + ")"
                count += 1

        elif (len(left_tuple) == 1):
            answer[0] =  answer[0] + "(" + left_tuple + "," + right_tuple + ")"
            count += 1
        else:
            if left_tuple not in answer[0] and right_tuple not in answer[0]:
                answer[0] = "(" + answer[0] + "," + right_tuple + ")"
                count += 1
    print 'Newick is wrong :(', answer[0]
    print 'Should be ((((A:8.5,B:8.5):2.5,E:11):5.5,(C:14,D:14):2.5)     '
    
    #print node_dict['ABCDE']

################################################################################################################################
# Have to use this line of code because our program needs to run with command line arguments
################################################################################################################################
if __name__ == "__main__":
    main()
