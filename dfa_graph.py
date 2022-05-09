import graphviz
import json
import networkx as nx
import matplotlib.pyplot as plt

with open('advs_transitions.json') as json_file:
    transition_dict = json.load(json_file)
    # print(transition_dict)

# Use Graphviz to create a graph
# dfa_dot = graphviz.Digraph("DFA", comment='DFA')

# for transition in transition_dict:
#     dfa_dot.node(transition)

# dfa_dot.render(directory='dfaDot-Output', view=True)


# # Use NetworkX to create a graph
# dfa_graph = nx.DiGraph()
# for transition in transition_dict:
#     dfa_graph.add_node(transition)
#     for next_state in transition_dict[transition]:
#         dfa_graph.add_edge(transition, transition_dict[transition][next_state], label=next_state)

# nx.draw(dfa_graph, with_labels=True)
# plt.savefig('dfa_graph.png')

