import pandas as pd
import numpy as np
import yaml
import uuid
from kisymbol.Sexpr import SexprBuilder

def rand_uuid():
    return str(uuid.uuid4())

def gen_pads(config, layers, b):
    for y in range(0, 16):
        for x in range(0, 16):
            b.open(f"pad \"{config.row_ids[y]}{x+1}\" smd circle")
            b.write(f"(at {format(((x - 7) * 0.8) - 0.4, '0.2f')} {format(((y - 7) * 0.8) - 0.4, '0.2f')})")
            b.write("(size 0.45 0.45)")
            b.write("(layers \"F.Cu\" \"F.Mask\" \"F.Paste\")")
            b.write(f"(uuid \"{rand_uuid()}\")")
            b.close()

def generate_property(property, value, y, layer, hide, b):
    b.open(f"property \"{property}\" \"{value}\"")
    b.write(f"(at 0 {y} 0)")
    b.write("(unlocked yes)")
    b.write(f"(layer \"{layer}\")")
    if hide:
        b.write("(hide yes)")
    b.write(f"(uuid \"{rand_uuid()}\")")
    b.open("effects")
    b.open("font")
    b.write("(size 1 1)")
    b.write("(thickness 0.1)")
    b.close()
    b.close()
    b.close()

def generate_footprint(config, df: pd.DataFrame):
    b = SexprBuilder()
    footprint = config.footprint.split(':')[1]
    b.open(f"footprint \"{footprint}\"")
    b.write("(version 20241209)")
    b.write("(generator \"wavelet_com_au\")")
    b.write("(layer \"F.Cu\")")
    generate_property("Reference", "REF**", -0.5,  "F.SilkS", False, b)
    generate_property("Value", footprint, 1,  "F.Fab", False, b)
    generate_property("Datasheet", "", 0,  "F.Fab", True, b)
    generate_property("Description", "", 0, "F.Fab", True, b)
    b.write("(attr smd)")
    gen_pads(config, "", b)
    b.close()
    print(b.render())

