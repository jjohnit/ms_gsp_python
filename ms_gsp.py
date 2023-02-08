# Initial pass to create initial candidate set
# sorted_items = list of itemsets sorted by min support
# sequences = list of all sequences
def init_pass(sorted_items, sequences):
    pass

# create a frequent item set
# items = list of itemset
# min_supports = min support of items
def initial_frequent_item_set(items, min_supports):
    pass

# Create the frequent item set using the candidate set and previous frequent set
def frequent_item_set(candidate_set, previous_frequent_set):
    pass

# Create lvl 2 candidate sequence 
def lvl_2_candidate_gen(sequences_2):
    pass

# for creating min support candidate sets
def ms_candidate_gen(frequent_set, min_supports):
    pass


# MS GSP algorithm with params
# sequences = list of all sequenses
# min_supports = list of all minimum supports
def ms_gsp(sequences, min_supports):
    # sort the itemsets in the sequences based on the ms value to create 'sorted_itemsets'
    sorted_itemsets = []
    # call init_pass(sorted_items, sequences) to generate initial candidate set
    candidate_sequence = init_pass(sorted_itemsets, sequences)
    # create frequent item set 1 with elements in candidate_sequence having min support
    frequent_items = initial_frequent_item_set(candidate_sequence, min_supports)

    candidate_sequence = lvl_2_candidate_gen(candidate_sequence)
    frequent_items = frequent_item_set(candidate_sequence, frequent_items)
    while(len(frequent_items) > 0):
        candidate_sequence = ms_candidate_gen(frequent_items, min_supports)
    pass