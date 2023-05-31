import sys
import lark
import svgwrite

# Definir la gramática de JFF
jff_grammar = """
    start: jff
    jff: machine | comment
    machine: "name" CNAME "type" ("fa" | "moore" | "mealy") "alphabet" alphabet? "states" states "transitions" transitions
    alphabet: "{" [SYMBOL ("," SYMBOL)*] "}"
    states: "{" CNAME ("," CNAME)* "}"
    transitions: "{" transition+ "}"
    transition: CNAME "->" CNAME ":" (SYMBOL | lambda)
    comment: /\/\/.*/
    SYMBOL: /[^\s->,{}]+/
    %import common.CNAME
    %import common.WS
    %ignore WS
"""

# Cargar el archivo JFF
with open(sys.argv[1], "r") as jff_file:
    jff_data = jff_file.read()

# Analizar el archivo JFF
jff_parser = lark.Lark(jff_grammar)
jff_tree = jff_parser.parse(jff_data)

# Inicializar un objeto SVG
svg_size = (500, 500)
dwg = svgwrite.Drawing(sys.argv[2], size=svg_size)

# Definir algunos valores útiles
state_radius = 20
state_font_size = 16

# Dibujar los estados
for state in jff_tree.find_data("states"):
    x = state.i * (svg_size[0] / len(state.children))
    y = state_radius + 20
    dwg.add(dwg.circle(center=(x, y), r=state_radius,
            fill="white", stroke="black"))
    dwg.add(dwg.text(state.children[0].value, insert=(
        x, y), text_anchor="middle", font_size=state_font_size))

# Dibujar las transiciones
for transition in jff_tree.find_data("transition"):
    from_state = transition.children[0].value
    to_state = transition.children[1].value
    label = transition.children[2].value
    from_x = from_state.i * (svg_size[0] / len(from_state.parent.children))
    to_x = to_state.i * (svg_size[0] / len(to_state.parent.children))
    midpoint = ((from_x + to_x) / 2, svg_size[1] / 2)
    label_offset = (midpoint[0] - (state_radius * 2),
                    midpoint[1] - state_font_size)
    dwg.add(dwg.line(start=(from_x, state_radius + 20),
            end=(to_x, state_radius + 20), stroke="black"))
    dwg.add(dwg.text(label, insert=label_offset,
            text_anchor="start", font_size=state_font_size))

# Guardar el archivo SVG
dwg.save()
