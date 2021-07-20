import random
from llist import dllist
from random import randint

def getCommonPairCodes(longpairs, shortpairs):
    return list(set([ i[5] for i in longpairs for j in shortpairs if i[5]==j[5]]))
    
        

def analyzeAndRandomize(longpairs, shortpairs):
    # identify the common pairs and shuffle them
    common_codes = getCommonPairCodes(longpairs, shortpairs)
    print('number of common pairs: ' + str(len(common_codes)))
    print('randomizing their order...')
    random.shuffle(common_codes)

    # place the common pairs in the new lists
    new_long_pairs = dllist()
    new_short_pairs = dllist()
    for code in common_codes:
        new_long_pairs.extend([ [pair[0], pair[1], pair[2], pair[3], pair[4], pair[5], 'FIXED'] for pair in longpairs if pair[5]==code])
        new_short_pairs.extend([[pair[0], pair[1], pair[2], pair[3], pair[4], pair[5], 'FIXED']  for pair in shortpairs if pair[5]==code])
    
    # shuffle the non-common pairs and add them to the list
    shuffleAdd(longpairs, new_long_pairs, common_codes)
    shuffleAdd(shortpairs, new_short_pairs, common_codes)

    return { 
        'longpairs':  [p for p in new_long_pairs], 
        'shortpairs': [p for p in new_short_pairs]
        }

# check for making sure no adjacent nodes with similar code.
def isAdjacentSimilar(llnode, pair):
    try:
        val1= (llnode.prev != None and llnode.prev.value[5].startswith(pair[5][0:2]))
        print('comparing ' + pair[5] + ' and prev ' + llnode.prev.value[5] + 'and the matching returns ' + str(val1))
        val2 = (llnode.value[5].startswith(pair[5][0:2]))
        print('comparing ' + pair[5] + ' and current ' + llnode.value[5] + 'and the matching returns ' + str(val2))
        val3 = val1 or val2
        print('final return val is ' + str(val3))
        return val3
    except AttributeError as e:
        print('sorry')
    return ((llnode.prev != None and llnode.prev.value[5].startswith(pair[5][0:2]))
        or (llnode.value[5].startswith(pair[5][0:2])))


# This function adds the non-common elements from pairs_list
# to new_pairs_list which is now a linked list.
def shuffleAdd(pairs_list, new_pairs_list, common_codes):
    random.shuffle(pairs_list)
    element = new_pairs_list.first
    uncommon_pairs = [pairs for pairs in pairs_list if pairs[5] not in common_codes]
    problems = 0
    for pair in uncommon_pairs:

        # val = isAdjacentSimilar(element, pair)
        # try:
        #     print(pair[5] + "   prev is  " + element.value[5][0:2] + ' next is  ' + element.next.value[5][0:2] + ' flag is ' + str(val))
        # except AttributeError as e:
        #     print('an attribute error occured.')
        if(isAdjacentSimilar(element, pair)):
            # an adjacent element has the same question node. 
            flag = False
            initial = new_pairs_list.nodeat(randint(0, new_pairs_list.size-1))
            element = initial
            for x in range(0, new_pairs_list.size):
                if(isAdjacentSimilar(element, pair) == False):
                    flag = True
                    break 
                if(element.next == None):
                    element = new_pairs_list.nodeat(0)
                else:
                    element = element.next
            if flag:
                problems +=1
        new_pairs_list.insert(pair, element)
        element = element.next
        if(element == None):
            element = new_pairs_list.first
    print('shuffle add completed for one list. number of problematic additions: ' + str(problems))          
