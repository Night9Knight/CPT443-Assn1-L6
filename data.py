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

# # Add new adverbs which the dot symbol is removed
# new_advs = [adv.replace('.','') for adv in all_advs if '.' in adv]
# all_advs.extend(new_advs)

# # Replace underscore with space
# all_advs = [adv.replace('_',' ') for adv in all_advs]

# Store original list of adverbs
with open('adverbs_raw.txt', 'w') as f:
    for adv in all_advs:
        f.write(adv + '\n')

# Use regex to filter out adverbs that contains dots or other unwanted characters
filtered_all_advs = set([adv.strip().lower() for adv in all_advs if re.search(r"[!#\"$%&()*+,\/:;<=>?@\[\\\]^`{|}~]", adv) is None])

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
advs_transition_dict['<s>'] = {}
advs_start_letters = []

for adv in filtered_all_advs:
    if adv[0] not in advs_start_letters:
        advs_start_letters.append(adv[0])
    
    for i in range(len(adv)):
        # print("adv[:i+1] = ", adv[:i+1])
        if adv[:i+1] not in advs_transition_dict:
            advs_transition_dict[adv[:i+1]] = {}
        
        if adv[:i]!='':
            advs_transition_dict[adv[:i]][adv[i]] = adv[:i+1]

for letter in advs_start_letters:
    advs_transition_dict['<s>'][letter] = letter

with open("advs_transitions.json", "w") as outfile:
    json.dump(advs_transition_dict, outfile)

