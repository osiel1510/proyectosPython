import xml.etree.ElementTree as ET
import svgwrite

# Load the JFF file
tree = ET.parse('test3.jff')
root = tree.getroot()

# Find the automaton element
automaton = root.find('automaton')

# Find the states and transitions
states = automaton.findall('state')
transitions = automaton.findall('transition')


# Create the SVG file
dwg = svgwrite.Drawing('example.svg', size=('500px', '500px'))

# Draw the states
for state in states:
    x = float(state.find('x').text)
    y = float(state.find('y').text)
    r = 20
    dwg.add(dwg.circle(center=(x, y), r=r, fill='yellow', stroke='black'))
    dwg.add(dwg.text(state.get('name'), insert=(x, y),
            text_anchor='middle', alignment_baseline='middle'))

# Draw the transitions
for transition in transitions:
    from_state = transition.find('from').text
    to_state = transition.find('to').text
    symbol = transition.find('read').text or 'ε'
    if symbol == 'ε':
        continue  # Skip epsilon transitions
    path = dwg.path(fill='none', stroke='black', stroke_width=1)
    start_x = float(automaton.find(f'state[@id="{from_state}"]/x').text)
    start_y = float(automaton.find(f'state[@id="{from_state}"]/y').text)
    end_x = float(automaton.find(f'state[@id="{to_state}"]/x').text)
    end_y = float(automaton.find(f'state[@id="{to_state}"]/y').text)
    if from_state != to_state:
        path.push(f'M{start_x},{start_y} L{end_x},{end_y}')
        path.set_markers(dwg.marker(refX='8', refY='5', markerWidth='6', markerHeight='6',
                                    orient='auto', viewBox='0 0 10 10', id='arrowhead'))
    else:
        # Self-loop
        r = 20
        path.push(
            f'M{start_x-r},{start_y} A{r},{r} 0 0,1 {start_x+r},{start_y} A{r},{r} 0 0,1 {start_x-r},{start_y}')
        path.set_markers(dwg.marker(refX='8', refY='5', markerWidth='6', markerHeight='6',
                                    orient='auto', viewBox='0 0 10 10', id='arrowhead', markerUnits='strokeWidth'))

    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2
    dwg.add(dwg.text(symbol, insert=(mid_x, mid_y),
            text_anchor='middle', alignment_baseline='middle'))
    dwg.add(path)

# Save the SVG file
dwg.save()
