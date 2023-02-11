# importing modules
import re


# Initial pass to create initial candidate set
# sorted_items = list of itemsets sorted by min support
# sequences = list of all sequences
def init_pass(sorted_items, sequences):
    for item in sorted_items:
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
    #sorted_itemsets = []
    # call init_pass(sorted_items, sequences) to generate initial candidate set
    candidate_sequence = init_pass(sorted_itemsets, sequences)
    # create frequent item set 1 with elements in candidate_sequence having min support
    frequent_items = initial_frequent_item_set(candidate_sequence, min_supports)

    candidate_sequence = lvl_2_candidate_gen(candidate_sequence)
    frequent_items = frequent_item_set(candidate_sequence, frequent_items)
    while(len(frequent_items) > 0):
        candidate_sequence = ms_candidate_gen(frequent_items, min_supports)
    pass



# Function for sorting the itemsets       
def sort_itemsets(I):
    minsup_items=[]
    for item in I:
        item1=item[1:]
        item1=item1[:-1]
        each=item1.split(',')
        minsup=1
        for val in each:
            val=val.strip()
            if mis[val]<minsup:
                minsup=mis[val]
        minsup_items.append(minsup)
    
    print(I)
    minsup_items.sort()
    print(minsup_items)
    sorted_itemsets = [i for _,i in sorted(zip(minsup_items,I))]
    return sorted_itemsets, minsup_items    


#Pre-processing of data
f = open("para1.txt", "r")
lines=f.readlines()
mis={}
SDC=0

for line in lines:
    misRegex = re.compile(r'MIS\((\d+)\) = (\d+.\d+)')
    mo=misRegex.search(line)
    if mo!=None:
        mis[mo.group(1)]=float(mo.group(2))
    misRegex = re.compile(r'SDC = (\d+.\d+)')
    mo=misRegex.search(line)
    if mo!=None:
        SDC=float(mo.group(1))

f.close()

f=open("data1.txt","r")
seqs=f.readlines()
print(seqs)

I=[]

for seq in seqs:
    seqsRegex = re.compile(r'({.*})')
    mo=seqsRegex.search(seq)
    list1=mo.group(1).split('}');
    list1.pop()
    for i in list1:
        i+='}';
        I.append(i)

I=[*set(I)]
sorted_itemsets,minsup_items=sort_itemsets(I)
print(sorted_itemsets)
print(minsup_items)

