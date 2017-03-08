# this is a global variable with 1's for mismatches and 0s for matches.
default_score = {}
for c1 in 'ACTGU':
    default_score[c1]={}
    for c2 in 'ACTGU':
        if c1==c2: default_score[c1][c2]=1
        else: default_score[c1][c2]=-1



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
 


