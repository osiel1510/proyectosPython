import svgwrite
import xml.etree.ElementTree as ET

# Parsear el archivo XML
tree = ET.parse('test2.jff')
root = tree.getroot()

# Obtener los estados y transiciones del autómata
states = root.findall(".//state")
transitions = root.findall(".//transition")

# Crear el lienzo SVG
svg_document = svgwrite.Drawing(filename='automata.svg')

# Dibujar los estados como círculos
for state in states:
    x = float(state.find('x').text)
    y = float(state.find('y').text)
    name = state.attrib['name']
    svg_document.add(svg_document.circle(
        center=(x, y), r=30, stroke='black', fill='white'))
    svg_document.add(svg_document.text(
        name, insert=(x-5, y+5), font_size="15"))

# Dibujar las transiciones como líneas con etiquetas de texto
for transition in transitions:
    start_state = transition.find('from').text
    end_state = transition.find('to').text
    label = transition.find('read').text
    start_state_element = root.find(".//state[@id='" + start_state + "']")
    end_state_element = root.find(".//state[@id='" + end_state + "']")
    x1 = float(start_state_element.find('x').text)
    y1 = float(start_state_element.find('y').text)
    x2 = float(end_state_element.find('x').text)
    y2 = float(end_state_element.find('y').text)
    svg_document.add(svg_document.line(
        start=(x1, y1), end=(x2, y2), stroke='black'))
    svg_document.add(svg_document.text(label, insert=(
        (x1+x2)/2 - 5, (y1+y2)/2 - 5), font_size="12"))

# Guardar el lienzo SVG como un archivo
svg_document.save()
