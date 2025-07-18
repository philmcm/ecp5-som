import pandas as pd
import numpy as np
import yaml
from kisymbol.Sexpr import SexprBuilder

def generate_rectangle(num_pins, b):
    b.open("rectangle")
    b.write("(start -6.35 -1.27)")
    # note: format(..., '.2f') required because 1.27*66 = 83.82000000000001
    b.write(f"(end 6.35 {format(2.54 * num_pins, '.2f')}")
    b.open("stroke")
    b.write("(width 0)")
    b.write("(type default)")
    b.close()
    b.open("fill")
    b.write("(type background)")
    b.close()
    b.close()

def generate_pins(unit, bank, config, df: pd.DataFrame, b):
    i = 0
    for index, row in df[df["Bank"]==bank].iterrows():
        b.open("pin bidirectional line")
	    # note: format(..., '.2f') required because 1.27*66 = 83.82000000000001
        b.write(f"(at -8.89 {format(i * 2.54, '.2f')} 0)")
        b.write("(length 2.54)")
        b.open(f"name \"{row["Function"]}\"")
        b.open("effects")
        b.open("font")
        b.write("(size 1.27 1.27)")
        b.close()
        b.close()
        b.close()
        b.open(f"number \"{index}\"")
        b.open("effects")
        b.open("font")
        b.write("(size 1.27 1.27)")
        b.close()
        b.close()
        b.close()
        b.close()
        i += 1
    return i

def generate_units(config, df: pd.DataFrame, b):
    for unit, bank in enumerate(df["Bank"].unique(), start=1):
        b.open(f"symbol \"{config.value}_{unit}_1\"")
        num_pins = generate_pins(unit, bank, config, df, b)
        generate_rectangle(num_pins, b)
        b.close()

def generate_symbol(config, df: pd.DataFrame, b):
    b.open(f"symbol \"{config.value}\"")

    # reference
    b.open("property \"Reference\" \"U\"")
    b.write("(at -8.89 16.51 0)")
    b.open("effects")
    b.open("font")
    b.write("(size 1.27 1.27)")
    b.close()
    b.close()
    b.close()

    # value
    b.open(f"property \"Value\" \"{config.value}\"")
    b.write("(at 7.62 -16.51 0)")
    b.open("effects")
    b.open("font")
    b.write("(size 1.27 1.27)")
    b.close()
    b.close()
    b.close()

    # footprint
    b.open(f"property \"Footprint\" \"{config.footprint}\"")
    b.write("(at 0 -36.83 0)")
    b.write("(show_name)")
    b.open("effects")
    b.open("font")
    b.write("(size 1.27 1.27)")
    b.close()
    b.write("(hide yes)")
    b.close()
    b.close()

    # datasheet
    b.open(f"property \"Datasheet\" \"{config.datasheet}\"")
    b.write("(at 1.27 -29.21 0)")
    b.write("(show_name)")
    b.open("effects")
    b.open("font")
    b.write("(size 1.27 1.27)")
    b.close()
    b.write("(hide yes)")
    b.close()
    b.close()

    generate_units(config, df, b)
    b.close()

def generate_symbol_library(config, df: pd.DataFrame):
    b = SexprBuilder()

    b.open("kicad_symbol_lib")
    b.write("(version 20241209)")
    b.write("(generator \"wavelet_com_au\")")
    generate_symbol(config, df, b)
    b.close()
    print(b.render())

