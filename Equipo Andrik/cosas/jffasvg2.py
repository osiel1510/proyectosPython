import graphviz
import xml.etree.ElementTree as ET

# Parse the JFLAP file
tree = ET.parse('Automata3.jff')
root = tree.getroot()

# Create a new GraphViz graph
graph = graphviz.Digraph(format='svg')

# Add the states to the graph
for state in root.findall('.//state'):
    state_id = state.get('id')
    state_name = state.get('name')
    is_initial = bool(state.find('initial'))
    is_final = bool(state.find('final'))

    # Add the state to the graph
    if is_initial and is_final:
        graph.node(state_id, label=state_name, shape='doublecircle')
    elif is_initial:
        graph.node(state_id, label=state_name, shape='circle', style='bold')
    elif is_final:
        graph.node(state_id, label=state_name, shape='doublecircle')
    else:
        graph.node(state_id, label=state_name, shape='circle')

# Add the transitions to the graph
for transition in root.findall('.//transition'):
    from_state = transition.find('from').text
    to_state = transition.find('to').text
    label = transition.find('read').text

    graph.edge(from_state, to_state, label=label)

# Render the graph and save it to a file
graph.render('file', view=True)
