#!/usr/bin/env python
from kisymbol import schematic, util

config = util.load_config('./config.yaml')
data = util.process_data(config.data_file)

# trim revision information
data = util.trim_to_header(data, "PAD")

bga256_df = (
    data[data['CABGA256'].astype(str).str.match(r'^[A-Z]+\d+$')]
    .drop(columns=[
        'CABGA554',
        'CABGA381',       
        'CSFBGA285',
        'TQFP144'])
    .reset_index(drop=True)
    .rename(columns={
        'CABGA256':'POS',
        'Pin/Ball Function':'Function',
        })
    [['PAD', 'POS', 'Function', 'Dual Function', 'Bank']]
)

schematic.generate_symbol_library(config, bga256_df)