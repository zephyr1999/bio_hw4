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

# this is a global variable with 1's for mismatches and 0s for matches.
default_score = {}
for c1 in 'ACTGU':
    default_score[c1]={}
    for c2 in 'ACTGU':
        if c1==c2: default_score[c1][c2]=1
        else: default_score[c1][c2]=-1


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

def global_dp_edit(seq1,seq2, gap_penalty, score=default_score):
    # Parameters: seq1, seq2 -> sequences to be matched
    #   score -> scoring matrix for mismatches.
    #
    # Note that this does score minimization, so the score matrix
    # given in the assignment must be inverted, i.e. each value
    # must be multiplied by - 1.
    #
    # this function uses dynamic programming to build a matrix
    # of edits and storing the backpointers to remember the
    # most optimal route. Each edit is only defined by the three
    # cells above, left, and up-left diagonal to it. After creating 
    # this matrix, it returns the minimum edit distance (the last
    # cell in the matrix) and the edited strings by tracing back
    # the most optimal route via backpointers. 
    #
    # Both its time and space complexity are len(seq1) x len(seq2) 
    # becasue both the edit matrix and the backpointer matrix are
    # of that size (memory) and that many operations are required to
    # fill them (time).

    # first, lets initialize our eeit and backpointer matricies.
    # note that both will have a +1 on their dimensions because
    # we need an extra column for initializations.
    # edit is the edit matrix, back is the backpointer one.
    edit = [[None for j in range(len(seq2)+1)] for i in range(len(seq1)+1)]
    back = [[None for j in range(len(seq2)+1)] for i in range(len(seq1)+1)]

    # now lets set their initial values. First up is edit.
    # edit's first column and first row are just the column or row index
    # respectively.
    edit[0] = [gap_penalty for i,_ in enumerate(edit[0])]
    for i,row in enumerate(edit):
        row[0] = gap_penalty
    edit[0][0] = 0
    
    
    # next up is pack. The top row of back is all left pointers (except 0,0)
    # and the first column is all up pointers (except 0,0)
    # 0,0 is a diagonal. For ease of debugging, I'll represent these as 'U'
    # for up, 'D' for diagonal, and 'L' for left. This makes nice prints.
    for i,row in enumerate(back):
        if i == 0:
            # this is the first row
            for j,_ in enumerate(row):
                back[i][j] = 'L'
        elif i > 0:
            # just set the first element to up
            row[0] = 'U'
    # we just want to initialize the 0,0 element
    back[0][0] = 'D'

    # now that we're all initializing, we can start to fill out everything!
    # we need to start from index 1 for both column and row, because we've 
    # already initialized the 0th column & row.
    for i in range(1,len(edit)):
        for j in range(1,len(edit[0])):
            # assign the current square just the minimum of (above+1), (left+1),
            # or (diagonal + penalty). Assign the backpointer the actual cell
            # that yields this minimum
            #
            # we'll keep track of this by just explicitly calculating these values.
            # Python could (of course) do this much more elegantly, but in this case
            # explicit is better.
            # don't forget to add the scoring penalty for the two characters!
            diagonal_score = edit[i-1][j-1] + score[seq1[i-1]][seq2[j-1]]
            # insertion penalties are just 1 so I don't feel bad about hardcoding these values.
            left_score = edit[i][j-1] + gap_penalty 
            up_score = edit[i-1][j] + gap_penalty

            # find the minimum and store it as our current value
            edit[i][j] = max([diagonal_score,left_score,up_score])
            # figure out which one is the max and store that as the backpointer.

            
 
    for i in range(1,len(edit)):
        for j in range(1,len(edit[0])):
            diagonal_score = edit[i-1][j-1]
            # insertion penalties are just 1 so I don't feel bad about hardcoding these values.
            left_score = edit[i][j-1]
            up_score = edit[i-1][j]
        
            max_score = max([diagonal_score,left_score,up_score])
            # figure out which one is the max and store that as the backpointer.
        
            if max_score == diagonal_score:
                back[i][j] = 'D'
            elif max_score == left_score:
                back[i][j] = 'L'
            else:
                back[i][j] = 'U'       
                
    # Now that we have the edit distance and the backpointer matrix, we can just 
    # follow back the backpointers and build our edited strings (in reverse 
    # order of course, because we have to start from the last element.
    edited_seq1 = ""
    edited_seq2 = ""

    # initialize the location to the bottom-right-most element
    location = (len(edit)-1,len(edit[0])-1)
    
    # now we just loop over backpointer, following its directions and making 
    # the appropriate additions to the edited sequences.
    while location != (0,0):
        if back[location[0]][location[1]] == 'D':
            # if we're at a d, we need to move up-left diagonally
            location = (location[0]-1,location[1]-1)
            # and diagonal means no alterations to either sequence. 
            # we do this step after the location has been modified because
            # the array indexes correspond to the sequence indexes+1
            edited_seq1 = seq1[location[0]] + edited_seq1
            edited_seq2 = seq2[location[1]] + edited_seq2
        elif back[location[0]][location[1]] == 'L':
            # we need to move left
            location = (location[0],location[1]-1)
            # left movement corresponds to adding a gap to seq1 and using the
            # normal character for seq2
            edited_seq2 = seq2[location[1]] + edited_seq2
            edited_seq1 = '-'+edited_seq1
        else:
            # we moved up, which is exactly equivalent to a left move
            # except we swap seq1 & seq2
            location = (location[0]-1,location[1])
            edited_seq1 = seq1[location[0]] + edited_seq1
            edited_seq2 = '-'+edited_seq2

    # and thats it! we just return the two edited sequences and the total editded distance.
    return edited_seq1,edited_seq2,edit[-1][-1]
 

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
    with open(filepath) as f:
        for dna_sequence in parse_file(f): #runs in O(n) sinc 
            array_of_seq.append(dna_sequence[1])
            

    #for every seq in the array go through and call global_dp_edit for 1 vs 2, 3 vs 4, until all seq have been delt with
    for i in range(0, len(array_of_seq)-1, 2):
        seq1, seq2, edit_distance = global_dp_edit(array_of_seq[i], array_of_seq[i+1], gap_penalty)
        #created a variable to know how many = to print out i final output
        number_equal_signs = len(seq1)
        #print   seq1
        #        seq2
        #        ===(#)
        print seq1 ,'\n', seq2 ,'\n', '='*number_equal_signs+'('+str(edit_distance)+')'
        
    #create empty array    
    answer = []
    #loop through list of seq and compare ever seq to eachother. Take the length of the seq returned
    #and divide number of matches by th elength to get a similarity score. Put score in array for each seq in order
    for i in array_of_seq:
        for j in array_of_seq:
            seq1, seq2, edit_distance = global_dp_edit(i, j, gap_penalty)
            answer.append( round(float(edit_distance)/float(len(seq1)), 5) )
    
    

    # length = len(array_of_seq)
    
    #np.array gets data ready to be a matrix
    #data = np.array( answer )
    #shape of matrix 
    #shape = ( length, length )
    #reshape matrix into the shpae we want number of seq by number of seq
    #data2 = data.reshape( shape )
    
    
    #print('\nAlignment Matrix')
    #print out matrix with format to align and add zeros to form 5 decimal float with tabs
    #print('\n'.join(['\t'.join(['{:<.5f}'.format(item) for item in row]) for row in data2]))

            
################################################################################################################################
# Have to use this line of code because our program needs to run with command line arguments
################################################################################################################################
if __name__ == "__main__":
    main()
