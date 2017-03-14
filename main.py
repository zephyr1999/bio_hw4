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

# this is a global variable with 1's for mismatches and 0s for matches.
#default_score = {}
#for c1 in 'ACTGU':
#    default_score[c1]={}
#    for c2 in 'ACTGU':
#        if c1==c2: default_score[c1][c2]=1
#        else: default_score[c1][c2]=-1


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
       
        
    #get absolute file path for filename    
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

    #list_of_stuff = ["A","B","C","D"]
    #numbers = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    dict1 = {}
    dict2 = {}

    for i in range(0, len(answer), 1):
        dict2[answer[i]] = {}
        for j in range(0, len(answer), 1):
            dict1[answer[j]] = int(new_r[i][j+1])
            dict2[answer[i]][answer[j]] = dict1[answer[j]]
                                        


    
    #############################################################################################################################
    #Still inside main, done with initial test. I call the parse_file generator in a for loop and it will yield back a seq
    #on every iteration. The seq is put into and array_of_seq
    #############################################################################################################################    
   
    #open file and loop through parsing out and returning the sequences
    array_of_seq = []
    array_of_seq_names = []
    with open(filepath) as f:
        for dna_sequence in parse_file(f): #runs in O(n) sinc 
            array_of_seq.append(dna_sequence[1])
            array_of_seq_names.append(dna_sequence[0])

    answer = []
    #loop through list of seq and compare ever seq to eachother. Take the length of the seq returned
    #and divide number of matches by th elength to get a similarity score. Put score in array for each seq in order
    
    for i in range(0, len(array_of_seq)):
        answer2 = []
        for j in range(i+1, len(array_of_seq)):
            edit_distance = global_dp_edit(array_of_seq[i], array_of_seq[j], gap_penalty, dict2)
            answer2.append( edit_distance )
        answer.append(answer2)
    
    answer = answer[::-1]
    
    
    

    
    print('\nDistance Matrix')
    #print out matrix with format to align and add zeros to form 5 decimal float with tabs
    print('\n'.join(['\t'.join(['{:<}'.format(item) for item in row]) for row in answer]))

            
    print '\n'
    print UPGMA(answer, array_of_seq_names)
    print '\n'
            
################################################################################################################################
# Have to use this line of code because our program needs to run with command line arguments
################################################################################################################################
if __name__ == "__main__":
    main()
