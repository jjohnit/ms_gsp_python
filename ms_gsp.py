# importing modules
import re


# Initial pass to create initial candidate set
# sorted_items = list of itemsets sorted by min support
# sequences = list of all sequences
def init_pass(sorted_items, seqs_list):
    L=[] 
    seqs1="".join(seqs)
    for item in sorted_items:
        supcnt[item]=(seqs1.count(item)/total_cnt)
    for seq in seqs_list:
        L_grp=[]
        for grp in seq:
            L_grp_item=[]
            min_sup=-1
            for item in grp:
                if min_sup==-1:
                    if supcnt[item]>=mis[item]:
                        L_grp_item.append(item)
                        min_sup=mis[item]
                    
                else:
                    if supcnt[item]>=min_sup:
                        L_grp_item.append(item)
            if L_grp_item!=[]:
                L_grp.append(L_grp_item)
        if L_grp!=[]:
            L.append(L_grp)
    print("L:")    
    print(L)
    return L
        
        
# create a frequent item set
# items = list of itemset
# min_supports = min support of items
def initial_frequent_item_set(L, mis):
    F1=[]
    
    for seq in L:
        for grp in seq:
            for item in grp:
                if supcnt[item]>=mis[item]:
                    F1.append(item)
    F1=[*set(F1)]
    print(F1)
    return F1

# Create the frequent item set using the candidate set and previous frequent set
def frequent_item_set(candidate_set, previous_frequent_set):
    pass

# Create lvl 2 candidate sequence 
def lvl_2_candidate_gen(L):
    C2=[]
    for seq in L:
        for grp in seq:
            for item in grp:
                if supcnt[item]>=mis[item]:
                    for i in range(grp.index(item)+1,len(grp)):
                        if ((supcnt[grp[i]]>=mis[item]) and (abs(supcnt[grp[i]]-supcnt[item])<=SDC)):
                                      C2.append([[item,grp[i]]])
                    for i in range(seq.index(grp)+1,len(seq)):
                        for item2 in seq[i]:
                            if ((supcnt[item2]>=mis[item]) and (abs(supcnt[item2]-supcnt[item])<=SDC)):
                                      C2.append([[item],[item2]])
                            
    print('C2:')
    C2.sort()
    k=0
    while k<len(C2) and k+1<len(C2):
        if C2[k]==C2[k+1]:
            del C2[k+1]
        else:
            k=k+1
    print(C2)
    return C2

# for creating min support candidate sets
def ms_candidate_gen(frequent_set, min_supports):
    pass


# MS GSP algorithm with params
# sequences = list of all sequenses
# min_supports = list of all minimum supports
def ms_gsp(sequences, min_supports):
    # sort the itemsets in the sequences based on the ms value to create 'sorted_itemsets'
    #sorted_itemsets = []
    sorted_itemsets=sort_itemsets(I)
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
def sort_itemsets(I):
    minsup_items=[]
    for item in I:
        minsup_items.append(mis[item])
    sorted_itemsets = [i for _,i in sorted(zip(minsup_items,I))]
    return sorted_itemsets   
    


#Pre-processing of data
para_file=str(input('Enter parameter file name:'))
data_file=str(input('Enter data file name:'))
f = open(para_file, "r")
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

f=open(data_file,"r")
seqs=f.readlines()

I=[]
seqs_list=[]
mis_list=[]
for seq in seqs:
    i_list=[]
    seqsRegex = re.compile(r'({.*})')
    mo=seqsRegex.search(seq)
    list1=mo.group(1).split('}');
    list1.pop()
    for i in list1:
        item_list=[]
        i=i[1:]
        i1=i.split(',')
        mis_list=[]
        for i1_item in i1:
            i1_item=i1_item.strip();
            item_list.append(i1_item)
            I.append(i1_item);
            mis_list.append(mis[i1_item])
        item_list = [i for _,i in sorted(zip(mis_list,item_list))]
        i_list.append(item_list)
    seqs_list.append(i_list)
total_cnt=len(seqs)
#print(seqs)
I=[*set(I)]
supcnt={}
ms_gsp(seqs_list,mis)