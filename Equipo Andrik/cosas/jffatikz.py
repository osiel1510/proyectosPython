import sys
import lark
from pytikz.generate import to_tikz

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

# Convertir el árbol JFF a código TikZ
tikz_code = to_tikz(jff_tree)

# Guardar el código TikZ en un archivo
with open(sys.argv[2], "w") as tikz_file:
    tikz_file.write(tikz_code)
