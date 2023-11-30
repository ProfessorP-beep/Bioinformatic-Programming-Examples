#Example to determine the gap penalty, mismatch penalty, and match reward
# Example: Determining Parameters for Needleman-Wunsch Alignment

def determine_alignment_parameters(seq1, seq2):
    # Analyze Sequence Characteristics
    similarity = sum(a == b for a, b in zip(seq1, seq2)) / len(seq1)
    evolutionary_distance = 1 - similarity

    # Adjust Parameters Based on Characteristics
    match_reward = 2  # Higher match reward for similar sequences
    mismatch_penalty = -1  # Lower mismatch penalty for similar sequences
    gap_penalty = -2 + evolutionary_distance  # Adjusted gap penalty based on evolutionary distance

    return match_reward, mismatch_penalty, gap_penalty

# Example Sequences
sequence1 = "AGTACGCA"
sequence2 = "AGTACGGA"

# Determine Parameters
match_reward, mismatch_penalty, gap_penalty = determine_alignment_parameters(sequence1, sequence2)

# Print Results
print("Match Reward:", match_reward)
print("Mismatch Penalty:", mismatch_penalty)
print("Gap Penalty:", gap_penalty)

#Create function to calculate alignment score
def needleman_wunsch(seq1, seq2, gap_penalty=-1.875, mismatch_penalty=-1, match_reward=2):
    len_seq1 = len(seq1)
    len_seq2 = len(seq2)

    # Initialize the score matrix
    score_matrix = [[0] * (len_seq2 + 1) for _ in range(len_seq1 + 1)]

    # Initialize the first row and column with gap penalties
    for i in range(len_seq1 + 1):
        score_matrix[i][0] = i * gap_penalty
    for j in range(len_seq2 + 1):
        score_matrix[0][j] = j * gap_penalty

    # Fill in the score matrix
    for i in range(1, len_seq1 + 1):
        for j in range(1, len_seq2 + 1):
            match = score_matrix[i - 1][j - 1] + (match_reward if seq1[i - 1] == seq2[j - 1] else mismatch_penalty)
            delete = score_matrix[i - 1][j] + gap_penalty
            insert = score_matrix[i][j - 1] + gap_penalty
            score_matrix[i][j] = max(match, delete, insert)

    # Traceback to find the aligned sequences
    aligned_seq1 = []
    aligned_seq2 = []
    i, j = len_seq1, len_seq2
    while i > 0 or j > 0:
        if i > 0 and j > 0 and score_matrix[i][j] == score_matrix[i - 1][j - 1] + (match_reward if seq1[i - 1] == seq2[j - 1] else mismatch_penalty):
            aligned_seq1.append(seq1[i - 1])
            aligned_seq2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and score_matrix[i][j] == score_matrix[i - 1][j] + gap_penalty:
            aligned_seq1.append(seq1[i - 1])
            aligned_seq2.append('-')
            i -= 1
        else:
            aligned_seq1.append('-')
            aligned_seq2.append(seq2[j - 1])
            j -= 1

    aligned_seq1.reverse()
    aligned_seq2.reverse()

    return ''.join(aligned_seq1), ''.join(aligned_seq2), score_matrix[len_seq1][len_seq2]

# Example usage
seq1 = "AGTACGCA"
seq2 = "TATGC"
aligned_seq1, aligned_seq2, alignment_score = needleman_wunsch(seq1, seq2)

print("Aligned Sequence 1:", aligned_seq1)
print("Aligned Sequence 2:", aligned_seq2)
print("Alignment Score:", alignment_score)
