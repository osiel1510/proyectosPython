import xml.etree.ElementTree as ET
import re
import math


class JFFtoSVGConverter:
    def __init__(self, jff_file_path, svg_file_path):
        self.jff_file_path = jff_file_path
        self.svg_file_path = svg_file_path
        self.svg_root = ET.Element('svg', attrib={
                                   'xmlns': 'http://www.w3.org/2000/svg', 'width': '1920', 'height': '1080'})
        self.svg_defs = ET.SubElement(self.svg_root, 'defs')

    def parse_jff_file(self):
        tree = ET.parse(self.jff_file_path)
        root = tree.getroot()

        arregloTransiciones = []

        for transition in root.findall('.//transition'):
            from_value = transition.find('from').text
            to_value = transition.find('to').text
            read_value = transition.find('read').text

            if from_value != to_value:

                from_estado = root.find(f".//state[@id='{from_value}']")
                to_estado = root.find(f".//state[@id='{to_value}']")

                from_x = float(from_estado.find('x').text)
                from_y = float(from_estado.find('y').text)
                to_x = float(to_estado.find('x').text)
                to_y = float(to_estado.find('y').text)

                # Calculate direction vector of the line
                dx = to_x - from_x
                dy = to_y - from_y
                length = ((dx ** 2) + (dy ** 2)) ** 0.5
                if length == 0:
                    length = 1 # set a default length
                direction_x = dx / length
                direction_y = dy / length


                # Calculate new points of the reduced line
                from_x_new = from_x + 20 * direction_x
                from_y_new = from_y + 20 * direction_y
                to_x_new = to_x - 20 * direction_x
                to_y_new = to_y - 20 * direction_y

                # Draw the transition line with reduced start and end
                transition_path = ET.SubElement(self.svg_root, 'path', attrib={
                    'd': f'M{from_x_new},{from_y_new} L{to_x_new},{to_y_new}',
                    'fill': 'none',
                    'stroke': 'black',
                    'stroke-width': '2',
                    'marker-end': 'url(#arrowhead)'
                })

                # Draw transition label
                transition_label_x = (from_x_new + to_x_new) / 2
                transition_label_y = (from_y_new + to_y_new) / 2

                # Calculate angle of the line
                angle = abs(math.atan2(dy, dx))

                # Calculate the perpendicular vector
                perpendicular_x = -direction_y
                perpendicular_y = direction_x

                repetido = arregloTransiciones.count([from_value,to_value])
                arregloTransiciones.append([from_value,to_value])

                # Adjust the position of the transition label based on the angle and the number of repetitions
                if angle >= math.pi / 4:
                    if to_y > from_y:
                        transition_label_x += 20
                        transition_label_anchor = 'start'
                    else:
                        transition_label_x -= 20
                        transition_label_anchor = 'end'
                else:
                    transition_label_y -= 20
                    transition_label_anchor = 'middle'

                # Update the transition_label position based on the perpendicular vector and the number of repetitions
                transition_label_x -= (20 * repetido * perpendicular_x)
                transition_label_y -= (20 * repetido * perpendicular_y)

                transition_label = ET.SubElement(self.svg_root, 'text', attrib={
                    'x': str(transition_label_x),
                    'y': str(transition_label_y),
                    'text-anchor': transition_label_anchor,
                    'dy': '.3em'
                })
                transition_label.text = read_value
            else:
                estado = root.find(f".//state[@id='{from_value}']")
                x_value = float(estado.find('x').text)
                y_value = float(estado.find('y').text)

                transition_loop = ET.SubElement(self.svg_root, 'ellipse', attrib={
                    'cx': str(float(x_value)+20), 'cy': str(y_value),
                    'rx': '30', 'ry': '15',
                    'fill': 'none',
                    'stroke': 'black',
                    'stroke-width': '2',
                    'transform': f'rotate(270 {x_value} {y_value})'
                })

                # Draw transition label
                repetido = arregloTransiciones.count([from_value,to_value])
                arregloTransiciones.append([from_value,to_value])

                y_value-= (20*repetido)

                transition_label = ET.SubElement(self.svg_root, 'text', attrib={
                    'x': str(x_value),
                    'y': str(y_value -60),
                    'text-anchor': 'middle',
                    'dy': '.3em'
                })
                transition_label.text = read_value

        # Loop through states
        for state in root.findall('.//state'):
            state_id = state.get('id')
            state_name = state.get('name')
            x_value = state.find('x').text
            y_value = state.find('y').text

            # Check if state is initial or final
            is_initial = False
            is_final = False
            for initial in state.findall('initial'):
                is_initial = True
            for final in state.findall('final'):
                is_final = True

            # Set state color based on type
            if is_initial and not is_final:
                state_color = 'green'
            elif not is_initial and is_final:
                state_color = 'red'
            else:
                state_color = 'yellow'

            # Draw state circle
            state_circle = ET.SubElement(self.svg_root, 'circle', attrib={
                'cx': str(x_value), 'cy': str(y_value), 'r': '20', 'fill': state_color, 'stroke': 'black'})

            # Draw state label
            state_label = ET.SubElement(self.svg_root, 'text', attrib={
                                        'x': str(x_value), 'y': str(y_value), 'text-anchor': 'middle', 'dy': '.3em'})
            state_label.text = state_id


    def add_arrowhead_marker(self):
        arrowhead_marker = ET.SubElement(self.svg_defs, 'marker', attrib={
                                         'id': 'arrowhead', 'viewBox': '0 0 10 10', 'refX': '8', 'refY': '5', 'markerWidth': '6', 'markerHeight': '6', 'orient': 'auto-start-reverse'})
        arrowhead_path = ET.SubElement(arrowhead_marker, 'path', attrib={
                                       'd': 'M 0 0 L 10 5 L 0 10 z'})

    def save_svg_file(self):
        self.add_arrowhead_marker()
        tree = ET.ElementTree(self.svg_root)
        tree.write(self.svg_file_path, xml_declaration=True,
                   encoding='utf-8', method='xml')


# Example usage
jff_file_path = 'test4.jff'
svg_file_path = 'example.svg'
converter = JFFtoSVGConverter(jff_file_path, svg_file_path)
converter.parse_jff_file()
converter.save_svg_file()
