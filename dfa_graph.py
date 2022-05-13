import json
import graphviz
import networkx as nx
import matplotlib.pyplot as plt

# Get first 15 adverbs
advs_list = []
with open('adverbs.txt') as f:
    advs_list = [word.strip() for word in f.readlines()][:15]
    print(len(advs_list))

# Run through list of adverbs and build a dictionary
advs_transition_dict = {}
advs_transition_dict['<s>'] = {}
advs_start_letters = []

for adv in advs_list:
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

# Use graphviz to draw the graph
dfa_dot = graphviz.Digraph("DFA", comment='DFA', format='png')
dfa_dot.node('fake', style='invis')
dfa_dot.edge('fake', graphviz.escape('<s>'))
dfa_dot.node(graphviz.escape('<s>'), root='true')
for transition in advs_transition_dict:
    if not advs_transition_dict[transition] or transition in advs_list:
        dfa_dot.node(transition, shape='doublecircle')
    
    for next_state in advs_transition_dict[transition]:
        dfa_dot.edge(graphviz.escape(transition), graphviz.escape(advs_transition_dict[transition][next_state]), label=graphviz.escape(next_state))
dfa_dot.render(directory='dfaDot-Output', view=True)

# # Use NetworkX to create a graph
# dfa_graph = nx.DiGraph()
# for transition in advs_transition_dict:
#     dfa_graph.add_node(transition)
#     for next_state in advs_transition_dict[transition]:
#         dfa_graph.add_edge(transition, advs_transition_dict[transition][next_state], label=next_state)

# nx.draw(dfa_graph, with_labels=True)
# plt.savefig('dfa_graph.png')

