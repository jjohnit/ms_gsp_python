# importing modules
import re


# Initial pass to create initial candidate set
# sorted_items = list of itemsets sorted by min support
# sequences = list of all sequences
def init_pass(sorted_items, seqs_list):
    L = []
    # seqs1="".join(seqs)
    # for item in sorted_items:
    #     supcnt[item]=(seqs1.count(item)/total_cnt)
    for seq in seqs_list:
        L_grp = []
        for grp in seq:
            L_grp_item = []
            min_sup = -1
            for item in grp:
                if min_sup == -1:
                    if supcnt[item] >= mis[item]:
                        L_grp_item.append(item)
                        min_sup = mis[item]

                else:
                    if supcnt[item] >= min_sup:
                        L_grp_item.append(item)
            if L_grp_item != []:
                L_grp.append(L_grp_item)
        if L_grp != []:
            L.append(L_grp)
    print("L:")
    print(L)
    return L


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


# MS GSP algorithm with params
# sequences = list of all sequenses
# min_supports = list of all minimum supports
def ms_gsp(sequences, min_supports, item_set, sup_count):
    # sort the items set in the sequences based on the ms value to create 'sorted_itemsets'
    #sorted_itemsets = []
    sorted_itemsets = sort_itemsets(item_set)
    # call init_pass(sorted_items, sequences) to generate initial candidate set
    L = init_pass(sorted_itemsets, sequences)
    # create frequent item set 1 with elements in candidate_sequence having min support
    F1 = initial_frequent_item_set(L, mis)
    # create candidate for level 2
    C2 = lvl_2_candidate_gen(L)


'''
    frequent_items = frequent_item_set(candidate_sequence, frequent_items)
    while(len(frequent_items) > 0):
        candidate_sequence = ms_candidate_gen(frequent_items, min_supports)
    pass
'''


# Function for sorting the itemsets
def sort_itemsets(item_set, mis):
    minsup_items = []
    for item in item_set:
        minsup_items.append(mis[item])
    sorted_itemsets = [i for _, i in sorted(zip(minsup_items, item_set))]
    return sorted_itemsets


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
    # print('sequence is ', item_sets)
    # Create the sequence as a list of item sets
    sequence_txt = item_sets.group(1).split('}')
    sequence = []
    # print('Sequence set is ', sequence_txt)
    # Removing the empty string at the end
    sequence_txt.pop()
    # print('Sequence set after popping is ', sequence_txt)
    for i in sequence_txt:
        item_list = []
        # Ignore the 1st char '{'
        i = i[1:]
        # For getting each item in the sequence
        items = i.split(',')
        # print('items is ', items)
        # mis_list = []
        # Create the item list as a list to be added to the sequence list
        for item in items:
            item = item.strip()
            item_list.append(item)
            all_items.add(item)
            # mis_list.append(min_supports[item])
        # print('All items list is ', all_items)
        # print('Item list before sorting ', item_list)
        # item_list = [i for _, i in sorted(zip(mis_list, item_list))]
        # print('Item list after sorting ', item_list)
        # sequence_of_sorted_items.append(item_list)
        # Add the item list to the sequence
        sequence.append(item_list)
    # all_sequences.append(sequence_of_sorted_items)
    # Add the sequence to all sequences
    all_sequences.append(sequence)
f.close()
print('Final sequences are ', all_sequences)
print('Final items are ', all_items)
# total_cnt=len(lines)
sequences_count = len(all_sequences)
print('Count of sequences is ', sequences_count)
# for i in all_sequences:
#     sequences_count += len(i)
# sup_count = {}
# seqs_text = "".join(lines)
# for item in all_items:
#     sup_count[item] = (seqs_text.count(item)/sequences_count)
# ms_gsp(all_sequences, min_supports, all_items, sup_count)
