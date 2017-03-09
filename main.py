# Homework 4
# Erik Holbrook Jorge Benavides Cosima Jackson
# test co
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
#    (e.g. python jorgebenavides_hw1.py -F <filename> 
################################################################################################################################

def usage():
    
    print '\npython jorgebenavides_hw2.py -F <filename> -L <size of k-mer> \n'
    print "where -F is the name of a FATSA format file to be read and analyzed"

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
            seq_name = line 
            seq = []
        else:
            seq.append(line)
    if seq_name: 
        #Since I skip the first if statement to wait for the seq to get filled in I have to make one last call in order to get
        #the last seq_name and seq
        yield (seq_name, ''.join(seq).upper())

def main():


    #create an instance of argument parser
    parse = argparse.ArgumentParser()
    
    #add arguments to parser so if command line argumnet matches -f or -F or --filename it will take the next argument
    #and put it into the --filename. See reference for more details on argparse.
    parse.add_argument('-F','-f', '--filename')
    parse.add_argument('-G','-g', '--gap')
    
    #create instance of parse_args
    args = parse.parse_args()
    
    #set the args to variable names for easy reference
    filename = args.filename
    gap_penalty = args.gap
    gap_penalty = int(gap_penalty)
    #error handling if any variables are empty something went wrong call usage function to inform user
    if(filename == None):
        usage()
        exit(2)
        
    #get absolute file path for filename    
    filepath = path.abspath(filename)

    
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

    #for every seq in the array go through and call global_dp_edit for 1 vs 2, 3 vs 4, until all seq have been delt with
    for i in range(0, len(array_of_seq)-1, 2):
        edit_distance = global_dp_edit(array_of_seq[i], array_of_seq[i+1], gap_penalty)
        #created a variable to know how many = to print out i final output
        #number_equal_signs = len(seq1)
        #print   seq1
        #        seq2
        #        ===(#)
        #print seq1 ,'\n', seq2 ,'\n', '='*number_equal_signs+'('+str(edit_distance)+')'
        
    #create empty array    
    answer = []
    #loop through list of seq and compare ever seq to eachother. Take the length of the seq returned
    #and divide number of matches by th elength to get a similarity score. Put score in array for each seq in order
    for i in array_of_seq:
        for j in array_of_seq:
            edit_distance = global_dp_edit(i, j, gap_penalty)
            answer.append( edit_distance )
    
    
    
    length = len(array_of_seq)
    
    #np.array gets data ready to be a matrix
    data = np.array( answer )
    #shape of matrix 
    shape = ( length, length )
    #reshape matrix into the shpae we want number of seq by number of seq
    data2 = data.reshape( shape )
    tri_lower_no_diag = np.tril(data2, k=0)

    
    print('\nDistance Matrix')
    #print out matrix with format to align and add zeros to form 5 decimal float with tabs
    print('\n'.join(['\t'.join(['{:<}'.format(item) for item in row]) for row in tri_lower_no_diag]))

    np.array(tri_lower_no_diag)
        
    new_array = tri_lower_no_diag.tolist()

    for i in new_array:
        while 0 in i:
            i.remove(0)
            
    print '\n'
    print UPGMA(new_array, array_of_seq_names )
    print '\n'
            
################################################################################################################################
# Have to use this line of code because our program needs to run with command line arguments
################################################################################################################################
if __name__ == "__main__":
    main()
