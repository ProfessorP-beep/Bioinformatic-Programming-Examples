#This script is to translate the python script with comments written with help
##From ChatGPT to R script to test if I understand the concepts and add a couple features to visualize the matrix and alignments.
#It creates a function that can align two sequences by creating a matrix with dynamic programming
library(stringr)
library(dplyr)
#Make simple assignments to test line by line as I code
seq_1 <- 'AGTACGCA' #sequence examples from ChatGPT
seq_2 <- 'TATGC'

#This was to test the function line by line
match_reward <- 1
mismatch_penalty <- -1
gap_penalty <- -1


#First going to create a function for sequence alignmnet
simple_alignment <- function(seq_1, seq_2, match_reward, mismatch_penalty, gap_penalty){
  #Need the sequence length by counting characters to create a matrix
  seq1_length <- nchar(seq_1)
  seq2_length <- nchar(seq_2)
  
  #Create the score matrix for alignment
  score_matrix <- matrix(0, ncol = seq1_length + 1, nrow = seq2_length + 1) 
  
  #add gap penalties to first row and column to account for gaps at the beginning of either sequence and to initialize matrix.
  score_matrix[1, ] <- seq(0, by = gap_penalty, length.out = seq1_length + 1) #column wise
  score_matrix[, 1] <- seq(0, by = gap_penalty, length.out = seq2_length + 1) #row wise
  
  #Begin to fill in the rows and columns with gap penalties
  for (x in seq(seq1_length)){  
    for (y in seq(seq2_length)){  
      match <- score_matrix[x-1, y-1] + ifelse(str_sub(seq_1, start = y-1, end = y-1) == str_sub(seq_2, start = x-1, end = x-1), match_reward, mismatch_penalty)
      deletion <- score_matrix[x-1, y] + gap_penalty
      insertion <- score_matrix[x, y-1] + gap_penalty
     
      score_matrix[x, y] <- max(match, deletion, insertion, na.rm = T)
  }
}
  
  #Traceback to find aligned sequences - reconstructs the aligned sequence by going backward through the matrix above.
  seq1_align <- character(0) #create empty character vectors to fill with the sequence
  seq2_align <- character(0)
  
    #add +1 to start at the bottom right corner of matrix                           
    i <- seq1_length + 1
    j <- seq2_length + 1
    
    #Create a loop that continues until i or j = 1
    while(i > 1 || j > 1){
      #if i > 1 and j > 1 AND there is a match, so can copy the match script from filling the rows above
      if(i > 1 && j > 1 && score_matrix[i-1, j-1] + ifelse(str_sub(seq_1, start = i-1, end = i-1) == str_sub(seq_2, start = j-1, end = j-1), match_reward, mismatch_penalty)){
      seq1_align <- c(seq1_align, str_sub(seq1_align, start =  i,end = i))
      seq2_align <- c(seq2_align, str_sub (seq2_align ,j-1, j-1))
      i <- i - 1 #update of indices i and j to move to the previous position in the matrix to refer to original sequence positions.
      j <- j - 1
      }else if(i > 1 && score_matrix[i, j] ==  score_matrix[i-1, j] + gap_penalty){ # mismatch - deletion
        seq1_align <- c(seq1_align, str_sub(i -1, i-1))
        seq2_align <- c(seq2_align, '-') #Fill gap in sequence from deletion
        i <- i - 1
      }else{ #insertion
        seq1_align <- c(seq1_align,'-')
        seq2_align <- c(seq2_align, str_sub(j-1, j-1)) #Fill gap in sequence from insertion.
        j <- j-1
      }
    }
    
    #Since the sequences were reconstructed in reverse in the traceback we have to reverse them to put them back into the right order
    seq1_align <- rev(seq1_align)
    seq2_align <- rev(seq2_align)
    
    #return the results of the alignment as a list object
    return(list(seq1_align = paste(seq1_align, collapse = ''),
                seq2_align = paste(seq1_align, collapse = ''),
                alignment_score = score_matrix[seq1_length + 1, seq2_length + 1]
                ))
  
}

simple_alignment(sequence_1, sequence_2, 1, -1, -1)
