import json
import re

def phrasel_search(P, Queries): 
    ans = []
    for query in Queries: # for each query
        another_tmp = []
        for phrase in P: # for each phrase 
            fuzzy = find_fuzzy(phrase, query) # find all the matches, fuzzy or not 
            if fuzzy:
                another_tmp.extend(fuzzy) # if fuzzy has things in it, add it to the list
        ans.append(another_tmp) # create a list inside the list
    return ans

def find_fuzzy(phrase, query):
    #split the strings
    word_split = phrase.lower().split()
    sentence = re.sub('[^a-zA-Z.\d\s]', '',query)
    sentence_split = sentence.lower().split()
    main, tmp, start, fuzz, space = [], [], 0, 0, " "
    try:
        # loop through entire sentence, from "starting" position
        while start < (len(sentence_split) - len(word_split)):
            if word_split[0] == sentence_split[start]:  # Did we find a match with the first word? cool
                tmp.append(word_split[0]) #put the first word in the list, instantiate both counters
                wcounter = 1
                scounter = 1
                for word in word_split[1:]:  # for each word in the phrase
                    if fuzz > 1: # check if our "fuzzy" has been used up, if it has, break for loop
                        break
                    elif sentence_split[start+scounter] == word_split[wcounter]: # Does the next word match?
                        tmp.append(word_split[wcounter])
                        wcounter += 1 # yeah? update counters, add word to tmp and go again
                        scounter += 1
                        continue
                    elif sentence_split[start+scounter+1] == word_split[wcounter] and start < len(sentence_split) - len(word_split): # no? time for fuzzy search. Does the word AFTER THAT match?
                        tmp.append(sentence_split[start+scounter])
                        tmp.append(word_split[wcounter])
                        wcounter += 1    # yes? ok, update fuzzy and counters, and go to next word
                        scounter += 2
                        fuzz += 1
                        continue
                    else: #Nothing matches? Update start to new position and add items to temp list
                        tmp = []
                        break
                if not tmp:   #if youre here we made it out of the forloop! does tmp hold anything?
                    start +=1 # then tmp is empty, we update start and go AGANE
                else:
                    tmp = space.join(tmp) # make the list a string so it can fit the answer easier
                    main.append(tmp) # append string into main [] 
                    for i in range(start, start+wcounter, 1): # Remove found elements from sentence_split
                        sentence_split.pop(start)
                    tmp = []
            else: # if nothing happens, we go AGANE
                start+=1
        return main # if something happens, we return MAIN           
    except ValueError: # if we get a value error at any point, return a blank list, probably a better solution somewhere out there /shrug
        return []

# easy lil testing def
def do_they_match(list1, list2):
    for list in list1:
        list.sort()
    for list in list2:
        list.sort()
    return list1, list2

if __name__ == "__main__":
    with open('30_points.json', 'r') as f:
        sample_data = json.loads(f.read())
        P, Queries = sample_data['phrases'], sample_data['queries']
        returned_ans = phrasel_search(P, Queries)
        sample_data['solution'], returned_ans = do_they_match(sample_data['solution'], returned_ans)
        print('============= ALL TEST PASSED SUCCESSFULLY ===============')
