# importing modules
import re


# Initial pass to create initial candidate set
# sorted_items = list of itemsets sorted by min support
# sequences = list of all sequences
def init_pass(sorted_items, sequences):
    L=[] 
    total=len(sequences)
    seqs=''.join(sequences)
    supcnt={}
    for item in sorted_items:
        cnt=seqs.count(item)
        supcnt[item]=(cnt/total)  
        
    for item_list in seqs_list:
        L1=[]
        minsup=-1
        for item in item_list:
            ind=sorted_items.index(item)
            if minsup!=-1:
                if supcnt[item]>=minsup:
                    L1.append(item)
            
        
        
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
        minsup_items.append(mis[item])
    sorted_itemsets = [i for _,i in sorted(zip(minsup_items,I))]
    return sorted_itemsets   
    


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

I=[]
seqs_list=[]

for seq in seqs:
    item_list=[]
    seqsRegex = re.compile(r'({.*})')
    mo=seqsRegex.search(seq)
    list1=mo.group(1).split('}');
    list1.pop()
    for i in list1:
        i=i[1:]
        i1=i.split(',')
        for i1_item in i1:
            i1_item=i1_item.strip();
            item_list.append(i1_item)
            I.append(i1_item);
    seqs_list.append(item_list)

I=[*set(I)]
sorted_itemsets=sort_itemsets(I)
print(sorted_itemsets)

#ms_gsp(seqs,mis)