# importing modules
import re
import copy


# Initial pass to create initial candidate set
# sorted_items = list of items sorted by min support
# seqs_list = list of all sequences
# min_support = minimum support
def init_pass(sorted_items, all_sequences, min_support):
    init_candidate_set = []
    print('Minimum support is ', min_support)
    total_sequences = len(all_sequences)
    # Find support count of each item by iterating through the sequences
    support_counts = {}
    for item in sorted_items:
        for seq in all_sequences:
            for itemset in seq:
                if(item in itemset):
                    support_counts[item] = 1 if(support_counts.get(item) == None) else (support_counts[item] + 1)
                    break                    
    print('Support counts are ', support_counts)
    # Convert the support count to percentage
    for key in support_counts.keys():
        support_counts[key] = support_counts[key] / total_sequences
    # Add items with minimum support to the init_candidate_set
    for item in sorted_items:
        if support_counts[item] >= min_support:
            init_candidate_set.append(item)

    print("Initial candidate set is ", init_candidate_set)
    return init_candidate_set, support_counts


#region create initial frequent item set
# items = list of itemset
# min_supports = min support of items
# def initial_frequent_item_set(candidate_set, min_supports, support_counts):
#     freq_item_set = set()
#     for seq in candidate_set:
#         # Initial candidate set contains items instead of item sets
#         if support_counts[item] >= min_supports[item]:
#             freq_item_set.add(item)
#     print("Frequent item set 1 is ", freq_item_set)
#     return freq_item_set
#endregion


#region Create lvl 2 candidate sequence
# def lvl_2_candidate_gen(L):
#     C2 = []
#     for seq in L:
#         for grp in seq:
#             for item in grp:
#                 if supcnt[item] >= mis[item]:
#                     for i in range(grp.index(item)+1, len(grp)):
#                         if ((supcnt[grp[i]] >= mis[item]) and (abs(supcnt[grp[i]]-supcnt[item]) <= SDC)):
#                             C2.append([[item, grp[i]]])
#                     for i in range(seq.index(grp)+1, len(seq)):
#                         for item2 in seq[i]:
#                             if ((supcnt[item2] >= mis[item]) and (abs(supcnt[item2]-supcnt[item]) <= SDC)):
#                                 C2.append([[item], [item2]])
#     print('C2:')
#     C2.sort()
#     k = 0
#     while k < len(C2) and k+1 < len(C2):
#         if C2[k] == C2[k+1]:
#             del C2[k+1]
#         else:
#             k = k+1
#     print(C2)
#     return C2
#endregion

# Create lvl 2 candidate sequence
def lvl_2_candidate_gen(freq_item_set, sup_counts, sdc):
    candidate_list = []
    for i in range(len(freq_item_set) - 1):
        #We also need to consider the case where both items are same
        #As per the example given in project spec
        candidate_list+=[[[freq_item_set[i]], [freq_item_set[i]]]]
        for j in range(i + 1, len(freq_item_set)):
            if(abs(sup_counts[freq_item_set[j]] - sup_counts[freq_item_set[i]]) <= sdc):
                candidate_list += [[[freq_item_set[i], freq_item_set[j]]], [[freq_item_set[i]], [freq_item_set[j]]]]
                #Also consider reverse order in sequence
                candidate_list +=[[[freq_item_set[j]], [freq_item_set[i]]]]
    print("Level 2 candidate list is ", candidate_list)
    return candidate_list

# for creating min support candidate sets
def ms_candidate_gen(freq_item_set, min_supports,sdc):
    candidate_sequence=[]
    
    for seq1 in freq_item_set:
        for seq2 in freq_item_set:
            seq1_copy=copy.deepcopy(seq1)
            #First and last elements of seq1
            first_seq1=seq1_copy[0][0]
            last_seq1=seq1_copy[-1][-1]
            # last_seq1=seq1_copy[len(seq1_copy)-1][len(seq1_copy[len(seq1_copy)-1])-1]
            
            seq2_copy=copy.deepcopy(seq2)
            #First and last elements of seq2
            first_seq2=seq2_copy[0][0]
            last_seq2=seq2_copy[-1][-1]
            # last_seq2=seq2_copy[len(seq2_copy)-1][len(seq2_copy[len(seq2_copy)-1])-1]
            
            if min_supports[first_seq1] < least_mis_sequence(seq1, 0, 0):
                seq1_copy[0].pop(0)
                '''
                if len(seq1_copy[0])>1:
                    seq1_copy[0].pop(1)
                else:
                    seq1_copy[1].pop(0)
                '''    
                seq1_copy = [ele for ele in seq1_copy if ele != []]
                seq2_copy[-1].pop(-1)
                # seq2_copy[len(seq2_copy)-1].pop(len(seq2_copy[len(seq2_copy)-1])-1)
                seq2_copy = [ele for ele in seq2_copy if ele != []]
                
                if seq1_copy==seq2_copy and min_supports[first_seq1]<min_supports[last_seq2]:
                    # if (len(seq2[len(seq2)-1]))==1:
                    if (len(seq2[-1])) == 1:
                        seq_copy=copy.deepcopy(seq1)
                        seq_copy+=[[last_seq2]]
                        candidate_sequence+=[seq_copy]
                        
                        if len(seq1)==2 and length_sequence(seq1)==2 and min_supports[last_seq2]>min_supports[last_seq1]:
                            seq_copy=copy.deepcopy(seq1)
                            seq_copy[len(seq_copy)-1].append(last_seq2)
                            candidate_sequence+=[seq_copy]
                    elif ((len(seq1)==1 and length_sequence(seq1)==2) and (min_supports[last_seq2]>min_supports[last_seq1])) or length_sequence(seq1)>2:
                        # last items of s1 & s2 has to be checked, not their minimum supports ?
                        seq_copy=copy.deepcopy(seq1)
                        seq_copy[-1].append(last_seq2)
                        # seq_copy[len(seq_copy)-1].append(last_seq2)
                        candidate_sequence+=[seq_copy]
            # elif min_supports[last_seq2] < least_mis_sequence(seq2,len(seq2)-1,len(seq2[len(seq2)-1])-1):
            elif min_supports[last_seq2] < least_mis_sequence(seq2,len(seq2)-1,len(seq2[-1])-1):
                seq2_copy[0].pop(0)
                '''
                if len(seq2_copy[0])>1:
                    seq2_copy[0].pop(1)
                else:
                    seq2_copy[1].pop(0)
                '''
                seq2_copy = [ele for ele in seq2_copy if ele != []]
                seq1_copy[len(seq1_copy)-1].pop(len(seq1_copy[len(seq1_copy)-1])-1)
                seq1_copy = [ele for ele in seq1_copy if ele != []]
                if seq1_copy==seq2_copy and min_supports[first_seq1]>min_supports[last_seq2]:
                    if (len(seq1[len(seq1)-1]))==1:
                        seq_copy=copy.deepcopy(seq2)
                        seq_copy+=[[first_seq1]+seq_copy]
                        candidate_sequence+=[seq_copy]
                        
                        if len(seq2)==2 and length_sequence(seq2)==2 and min_supports[last_seq1]>min_supports[last_seq2]:
                            seq_copy=copy.deepcopy(seq2)
                            seq_copy[len(seq_copy)-1]=first_seq1+seq_copy[len(seq_copy)-1]
                            candidate_sequence+=[seq_copy]
                    elif ((len(seq2)==1 and length_sequence(seq2)==2) and (min_supports[last_seq1]>min_supports[last_seq2])) or length_sequence(seq2)>2:
                        seq_copy=copy.deepcopy(seq2)
                        seq_copy[len(seq_copy)-1]=first_seq1+seq_copy[len(seq_copy)-1]
                        candidate_sequence+=[seq_copy]
            else:
                seq1_copy[0].pop(0)
                '''
                if len(seq1_copy[0])>1:
                    seq1_copy[0].pop(1)
                else:
                    seq1_copy[1].pop(0)
                '''
                seq1_copy = [ele for ele in seq1_copy if ele != []]
                seq2_copy[-1].pop(len(seq2_copy[-1])-1)
                # seq2_copy[len(seq2_copy)-1].pop(len(seq2_copy[len(seq2_copy)-1])-1)
                seq2_copy = [ele for ele in seq2_copy if ele != []]
                if seq1_copy==seq2_copy:
                    # if (len(seq2[len(seq2)-1]))==1:
                    if (len(seq2[-1]))==1:
                        seq_copy=copy.deepcopy(seq1)
                        seq_copy+=[[last_seq2]]
                        candidate_sequence+=[seq_copy]
                    else:
                       seq_copy=copy.deepcopy(seq1)
                       seq_copy[-1].append(last_seq2)
                    #    seq_copy[len(seq_copy)-1].append(last_seq2)
                       candidate_sequence+=[seq_copy] 
                        
    #print("Candidate sequences before pruning:",candidate_sequence)
    
    #Pruning step
    final_candidate_sequence = []
    for seq in candidate_sequence:
        temp_can_seq_list = []
        for i in range(0,len(seq)):
            least_mis_item=seq[i][0]
            highest_mis_item=seq[i][0]
            for item in seq[i]:
                if(min_supports[item] < min_supports[least_mis_item]):
                    least_mis_item = item
                if(min_supports[item] > min_supports[highest_mis_item]):
                    highest_mis_item = item
            for j in range(0,len(seq[i])):
                temp_can_seq = copy.deepcopy(seq)
                #We need not check the k-1 subsequences which contain the item with minimum MIS value
                #Hence, we do not create temp sequence for the sequence that contains the item with minimum MIS
                if(temp_can_seq[i][j] != least_mis_item):
                    temp_can_seq[i].pop(j)
                    temp_can_seq = [ele for ele in temp_can_seq if ele != []]
                    temp_can_seq_list.append(temp_can_seq)
        #print('Temp k-1 subsequences list:',temp_can_seq_list)
        flag=0
        #print('Pruned candidate sequences')
        for temp_seq in temp_can_seq_list:
            if temp_seq not in freq_item_set:
            #if any of the K-1 subsequences not in the K-1 candidate list then set flag to 1    
                flag=1
                #print(seq)
        if flag!=1 & (min_supports[highest_mis_item] - min_supports[least_mis_item] <= sdc):
            final_candidate_sequence.append(seq)
    #print("Candidate sequences after pruning:",final_candidate_sequence)
    return final_candidate_sequence                
                
                
            
        
# Function for sorting the items based on the minimum support
def sort_items(all_items, min_supports):
    minsup_items = []
    for item in all_items:
        minsup_items.append(min_supports[item])
    sorted_items = [i for _, i in sorted(zip(minsup_items, all_items))]
    return sorted_items



# Find least MIS value in a sequence excluding the MIS of the value 
# at 'index1' and 'index2'
def least_mis_sequence(seq,index1,index2):
    #least_mis=1
    if index1!=None and index2!=None:
        seq_copy=copy.deepcopy(seq)
        seq_copy[index1].pop(index2)
        least_mis=min_supports[seq[0][0]]
        for grp in seq_copy:
            for item in grp:
                if min_supports[item]<least_mis:
                    least_mis=min_supports[item]
    else:
        least_mis=min_supports[seq[0][0]]
        seq_copy=copy.deepcopy(seq)
        for grp in seq_copy:
            for item in grp:
                if min_supports[item]<least_mis:
                    least_mis=min_supports[item]
    return least_mis

#Function that returns length of a sequence
def length_sequence(seq):
    length=0
    for grp in seq:
        length+=len(grp)
    return length

'''
# To check whether a subsequence is present in a sequence
# eg: subsequence = [['20', '30', '70']] or [['20', '30'], ['90']]
# eg sequence = [['20', '30'], ['70', '80'], ['20', '30', '70']]
def is_contained(sequence, subsequence):
    # If the subsequence contain only one list
    if len(subsequence) == 1:
        # Check whether each item of subsequence is present in the sequence in the same order
        for seq in sequence:
            flag = False
            for item in subsequence[0]:
                # if item is in the sequence, check whether the remaining items comes after in the sequence
                # slice the seq list from the occurance of the element of this  
                if item in seq:
                    seq = seq[seq.index(item):]
                    flag = True
                # If the item is not present in the sequence, check for the same in the next seq
                else:
                    flag = False
                    break
            # If flag is true after checking all items in the subsequence with a sequence, then return true
            if flag:
                return True
        return False
    # If the subsequence contains multiple lists
    else:
        flag = False
        group = seq = 0
        # print("Seq len ", len(sequence)," group len ", len(subsequence))
        while((group < len(subsequence)) & (seq < len(sequence))):
            # print("Seq is ", sequence[seq]," group is ", subsequence[group])
            # If the subsequence group present in sequence group, check for the 
            # next subsequence group in the next sequence group
            if is_contained([sequence[seq]], [subsequence[group]]):   # Converted to a list of list since the function is expecting that
                flag = True
                group += 1
                seq += 1
            # If the subsequence group not present in sequence group, check for the 
            # same subsequence group in the next sequence group
            else:
                flag = False
                seq += 1
        return flag
'''        
# Rewriting the function for testing purpose    
def is_contained(sequence,subsequence):
    i=0
    count=0
    j=0
    #print('Subsequence:',subsequence)
    #print('Sequence:',sequence)
    while(j<len(subsequence)):
        while(i<len(sequence)):
            group=sequence[i]
            if j>=len(subsequence):
                break
            group_sub=subsequence[j]
            #If all items of group_sub also in group
            #Go to next group and sub-group
            if all(item in group for item in group_sub):
                count=count+1;
                i+=1
                j+=1
            #else case 
            #Go to next group, sub-group remains same
            else:
                i+=1
        j+=1
    
    if count==len(subsequence):
        return True
    else:
        return False
    
# To find the item with minimum item support
def find_min_mis_item(candidate, min_supports):
    if(len(candidate) == 1):
        min_mis_item = candidate[0][0]
        for item in candidate[0]:
            if min_supports[item] < min_supports[min_mis_item]:
                min_mis_item = item
        return min_mis_item
    else:
        min_mis_item = candidate[0][0]
        for group in candidate:
            temp_item = find_min_mis_item([group], min_supports)
            if min_supports[temp_item] < min_supports[min_mis_item]:
                min_mis_item = temp_item
        return min_mis_item
            




# MS GSP algorithm with params
# sequences = list of all sequenses
# min_supports = list of all minimum supports
def ms_gsp(sequences, min_supports, all_items, sdc):
    #Final sequence of sequences
    final_sequences={}
    #Counter for k (k-sequence)
    k=1
    # sort the items set in the sequences based on the ms value to create 'sorted_itemsets'
    sorted_items = sort_items(all_items, min_supports)
    print('Items sorted based on minimum support: ', sorted_items)
    # call init_pass(sorted_items, sequences, minumum support) to generate initial candidate set
    init_candidate_list, support_counts = init_pass(sorted_items, sequences, min_supports[sorted_items[0]])
    # create frequent item set 1 with elements in candidate_sequence having min support
    # freq_item_set_1 = initial_frequent_item_set(init_candidate_list, min_supports, support_counts)
    freq_item_set = []
    for item in init_candidate_list:
        # Initial candidate set contains items instead of item sets
        if support_counts[item] >= min_supports[item]:
            freq_item_set.append(item)
    print("Frequent item set 1 is ", freq_item_set)
    final_sequences[k]=freq_item_set
    # Create level 2 candidate list
    # Why can't we pass frequent item set 1 instead of initial candidate set,
    # considering we are eliminating items based on support count in the function?
    candidate_sequence = lvl_2_candidate_gen(freq_item_set, support_counts, sdc)
    #frequent_items = frequent_item_set(candidate_list, support_counts, sdc)
    sequences_count = len(sequences)
    while len(freq_item_set) > 0:
        freq_item_set = []
        # Create frequent list from the candidate sequences
        # Iterate through each sequence in candidate sequences
        # eg candidate sequence: [[['20', '30', '70']], [['20', '30'], ['70']]]
       # print('Candidate sequence',candidate_sequence)
        #print('Frequent itemset',freq_item_set)
        for candidate in candidate_sequence:
            # Find the candidate with min
            candidate_count = 0
            # Iterate through each sequence in all sequence list  
            # eg all sequences: [[['10', '40', '50'], ['40', '90']], [['20', '30'], ['70', '80'], ['20', '30', '70']]]
            for seq in sequences:
                # If the candidate is present in the sequence, increment the count
                if is_contained(seq, candidate):
                    candidate_count += 1
            
            min_mis_item = find_min_mis_item(candidate, min_supports)
            # Add the candidate to frequent item set
            if (candidate_count / sequences_count) > min_supports[min_mis_item]:
                freq_item_set.append(candidate)
        print('Frequent itemset:',freq_item_set)
        if len(freq_item_set) <= 0:
            break
        else:
            k+=1
            final_sequences[k]=freq_item_set
        candidate_sequence = ms_candidate_gen(freq_item_set, min_supports, sdc)
        print('Candidate sequence',candidate_sequence)
    return final_sequences        
    



# Pre-processing of data
# File with sequences (eg: <{10, 40, 50}{40, 90}> <{20, 30}{70, 80}{20, 30, 70}>)
# sequences_file=str(input('Enter sequences file name:'))
sequences_file = 'data2.txt'
# File minimum item supports (eg: MIS(10) = 0.45 MIS(20) = 0.30)
# minsups_file=str(input('Enter minimum supports file name:'))
minsups_file = 'para2-1.txt'
# Open the file to read the lines
f = open(minsups_file, "r")
lines = f.readlines()
# Dictionary for storing the minimum supports for each item
min_supports = {}
sdc = 0

# Iterate through each line of the mminimum supports file to extract the minimum supports for every item
for line in lines:
    # Remove the spaces in each line to have a standard format
    line = line.replace(' ', '')
    # Regex to find the minimum supports. Group 1 is the item and group 2 is its minimum support
    mis_regex = re.compile(r'MIS\((\d+)\)=(\d+.\d+)')
    ms = mis_regex.search(line)
    if ms != None:
        # Group 1 is the item and group 2 is its minimum support
        min_supports[ms.group(1)] = float(ms.group(2))
        continue
    # If the line donot contain MIS, then check for SDC
    mis_regex = re.compile(r'SDC=(\d+.\d+)')
    ms = mis_regex.search(line)
    if ms != None:
        sdc = float(ms.group(1))

f.close()
print('Minimum supports are ', min_supports)
print('SDC is ', sdc)

f = open(sequences_file, "r")
# Read each line containing seperate sequences
lines = f.readlines()
# Item set for storing all seperate item (eg: {10, 40, 50,...})
all_items = set()

# List to store all sequences extracted from the file
all_sequences = []
for line in lines:
    # sequence_of_sorted_items = []
    seqs_regex = re.compile(r'({.*})')
    # Extract the item sets in each sequence
    item_sets = seqs_regex.search(line)
    # Create the sequence as a list of item sets
    if item_sets!=None:
        sequence_txt = item_sets.group(1).split('}')
    sequence = []
    # Removing the empty string at the end
    sequence_txt.pop()
    for i in sequence_txt:
        item_list = []
        # Ignore the 1st char '{'
        i = i[1:]
        # For getting each item in the sequence
        items = i.split(',')
        # Create the item list as a list to be added to the sequence list
        for item in items:
            item = item.strip()
            item_list.append(item)
            all_items.add(item)
        # Add the item list to the sequence
        sequence.append(item_list)
    # Add the sequence to all sequences
    all_sequences.append(sequence)
f.close()
print('Final sequences are ', all_sequences)
print('Final items are ', all_items)
# total_cnt=len(lines)
sequences_count = len(all_sequences)
print('Count of sequences is ', sequences_count)
final_sequences=ms_gsp(all_sequences, min_supports, all_items, sdc)

#Writing the output into file
output_file = 'output2-1.txt'
# Open the file to read the lines
f = open(output_file, "w")

#For k=1
k=1
f.write("\n*************")
f.write("\n"+str(k)+"-sequences")
for seq in final_sequences[k]:
    f.write("\n<")
    f.write("{"+str(seq)+"}")
    f.write(">")
f.write("\nThe count is "+str(len(final_sequences[k])))

#Looping over final_sequences
for k in range(2,len(final_sequences)+1):
    f.write("\n*************")
    f.write("\n"+str(k)+"-sequences")
    for seq in final_sequences[k]:
        f.write("\n<")
        for group in seq:
            group_str = str(group)
            group_str=group_str.replace("[","{")
            group_str=group_str.replace("]","}")
            f.write(group_str)
        f.write(">")
    f.write("\nThe count is "+str(len(final_sequences[k])))
f.close()    
    
    

#region Testing is_contained function
# print("True is ", is_contained([['10', '30'], ['70', '80'], ['20', '30', '70']], [['10', '30']]))
# print("True is ", is_contained([['20', '30'], ['70', '80'], ['20', '30', '70']], [['30', '70']]))
# print("False is ", is_contained([['20', '30'], ['70', '80'], ['20', '30', '70']], [['30', '20']]))
# print("False is ", is_contained([['20', '30'], ['20', '30', '70']], [['70', '80']]))

# print("True is ", is_contained([['20', '30'], ['70', '80'], ['20', '30', '70']], [['20', '30'], ['80']]))
# print("True is ", is_contained([['20', '30'], ['70', '80'], ['20', '30', '70']], [['80'], ['70']]))
# print("True is ", is_contained([['20', '30'], ['70', '80'], ['20', '30', '70']], [['30'], ['70', '80']]))
# print("True is ", is_contained([['20', '30'], ['70', '80'], ['20', '30', '70']], [['30'], ['20']]))
# print("False is ", is_contained([['20', '30'], ['70', '80'], ['20', '30', '70']], [['70'], ['70', '80']]))
# print("False is ", is_contained([['20', '30'], ['70', '80'], ['20', '40', '70']], [['70'], ['20', '30']]))
#endregion

#region Testing find_min_mis_item function
# print("20 is ", find_min_mis_item([['20', '40', '70']], min_supports))
# print("70 is ", find_min_mis_item([['40', '70', '20']], min_supports))
# print("20 is ", find_min_mis_item([['20', '70'], ['40']], min_supports))
# print("70 is ", find_min_mis_item([['70', '40'], ['20']], min_supports))
# print("70 is ", find_min_mis_item([['40', '70'], ['20']], min_supports))
# print("20 is ", find_min_mis_item([['40'], ['20', '70']], min_supports))
# print("20 is ", find_min_mis_item([['20'], ['70', '40']], min_supports))
# print("20 is ", find_min_mis_item([['20'], ['40', '70']], min_supports))
#endregion