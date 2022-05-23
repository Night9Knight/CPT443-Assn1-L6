import nltk
from nltk.corpus import wordnet as wn
import re
import json
nltk.download('wordnet')
nltk.download('omw-1.4')

# Get list of adverbs from wordnet
all_advs = []
for synset in wn.all_synsets('r'):
    all_advs.extend(synset.lemma_names())

# Store original list of adverbs
with open('adverbs_raw.txt', 'w') as f:
    for adv in all_advs:
        f.write(adv + '\n')

# Remove duplicate entries for all adverbs in lowercase
filtered_all_advs = set([adv.lower() for adv in all_advs])

print(len(filtered_all_advs))

# Write word list to file
with open('adverbs.txt', 'w') as f:
    for adv in sorted(filtered_all_advs, key=len):
        f.write(adv + '\n')

# Write list of adverbs with 2 or more words to file
with open('adverbs_multiwords.txt', 'w') as f:
    for adv in filtered_all_advs:
        if len(adv.split('_')) > 1:
            f.write(adv + '\n')

# Run through list of adverbs and build a dictionary
advs_transition_dict = {}
advs_transition_dict['<s>'] = {} # Start state
advs_start_letters = []

for adv in filtered_all_advs:
    # Append the first letter to the start letter list if it is not in the list 
    if adv[0] not in advs_start_letters:
        advs_start_letters.append(adv[0])
    
    for i in range(len(adv)):
        # Create the key and assign an empty dictionary as the value in the transition dictionary if the key with the substring of current adverb from index 0 to current index (inclusive) does not exist  
        if adv[:i+1] not in advs_transition_dict:
            advs_transition_dict[adv[:i+1]] = {}
        
        # If the substring of the current adverb from index 0 to current index (exclusive) is not empty, create a key of the name of the letter of current adverb at current index in the dictionary of the transition dictionary with the key of the name of the substring of current adverb from index 0 to current index (exclusive) and assign the substring of current adverb from index 1 to current index (inclusive) as the value
        if adv[:i]!='':
            advs_transition_dict[adv[:i]][adv[i]] = adv[:i+1]

# Create a key with the current letter as name and value in the dictionary of the transition dictionary with the start state as the key name. 
for letter in advs_start_letters:
    advs_transition_dict['<s>'][letter] = letter

# Save the transition dictionary as a JSON file
with open("advs_transitions.json", "w") as outfile:
    json.dump(advs_transition_dict, outfile)

