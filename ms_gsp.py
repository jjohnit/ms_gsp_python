# importing modules
import re


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
    # Add items with minimum support to the init_candidate_set
    for item in sorted_items:
        if (support_counts[item] / total_sequences) >= min_support:
            init_candidate_set.append(item)

    print("Initial candidate set is ", init_candidate_set)
    return init_candidate_set


# create a frequent item set
# items = list of itemset
# min_supports = min support of items
def initial_frequent_item_set(L, mis):
    F1 = []

    for seq in L:
        for grp in seq:
            for item in grp:
                if supcnt[item] >= mis[item]:
                    F1.append(item)
    F1 = [*set(F1)]
    print(F1)
    return F1

# Create the frequent item set using the candidate set and previous frequent set


def frequent_item_set(candidate_set, previous_frequent_set):
    pass

# Create lvl 2 candidate sequence


def lvl_2_candidate_gen(L):
    C2 = []
    for seq in L:
        for grp in seq:
            for item in grp:
                if supcnt[item] >= mis[item]:
                    for i in range(grp.index(item)+1, len(grp)):
                        if ((supcnt[grp[i]] >= mis[item]) and (abs(supcnt[grp[i]]-supcnt[item]) <= SDC)):
                            C2.append([[item, grp[i]]])
                    for i in range(seq.index(grp)+1, len(seq)):
                        for item2 in seq[i]:
                            if ((supcnt[item2] >= mis[item]) and (abs(supcnt[item2]-supcnt[item]) <= SDC)):
                                C2.append([[item], [item2]])

    print('C2:')
    C2.sort()
    k = 0
    while k < len(C2) and k+1 < len(C2):
        if C2[k] == C2[k+1]:
            del C2[k+1]
        else:
            k = k+1
    print(C2)
    return C2

# for creating min support candidate sets


def ms_candidate_gen(frequent_set, min_supports):
    pass

# Function for sorting the items based on the minimum support


def sort_items(all_items, min_supports):
    minsup_items = []
    for item in all_items:
        minsup_items.append(min_supports[item])
    sorted_items = [i for _, i in sorted(zip(minsup_items, all_items))]
    return sorted_items

# MS GSP algorithm with params
# sequences = list of all sequenses
# min_supports = list of all minimum supports


def ms_gsp(sequences, min_supports, all_items):
    # sort the items set in the sequences based on the ms value to create 'sorted_itemsets'
    sorted_items = sort_items(all_items, min_supports)
    print('Items sorted based on minimum support: ', sorted_items)
    # call init_pass(sorted_items, sequences, minumum support) to generate initial candidate set
    init_candidate_list = init_pass(
        sorted_items, sequences, min_supports[sorted_items[0]])
    # create frequent item set 1 with elements in candidate_sequence having min support
    # F1 = initial_frequent_item_set(init_candidate_list, min_supports)
    # create candidate for level 2
    # C2 = lvl_2_candidate_gen(init_candidate_list)


'''
    frequent_items = frequent_item_set(candidate_sequence, frequent_items)
    while(len(frequent_items) > 0):
        candidate_sequence = ms_candidate_gen(frequent_items, min_supports)
    pass
'''


# Pre-processing of data
# File with sequences (eg: <{10, 40, 50}{40, 90}> <{20, 30}{70, 80}{20, 30, 70}>)
# sequences_file=str(input('Enter sequences file name:'))
sequences_file = 'data1.txt'
# File minimum item supports (eg: MIS(10) = 0.45 MIS(20) = 0.30)
# minsups_file=str(input('Enter minimum supports file name:'))
minsups_file = 'para1.txt'
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
ms_gsp(all_sequences, min_supports, all_items)
