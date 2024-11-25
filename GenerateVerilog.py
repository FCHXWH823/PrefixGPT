import pandas as pd
import csv
import random
from PrefixCircuit import PrefixCircuit
import re
import os
bit_width = 8
level_limitation = 9

# verilog_path = f"ClassicalPCs/{bit_width}bit/KoggeStone{bit_width}.v"
# circuit = PrefixCircuit()
# circuit.build_kogge_stone_circuit(bit_width)
# circuit.generate_verilog(verilog_path)

# file_path = f"GPTPrefix{bit_width}_L{level_limitation}/GPTPrefix{bit_width}_L{level_limitation}_Pruned.txt"
# verilog_path = f"GPTPrefix{bit_width}_L{level_limitation}/GPTPrefix{bit_width}_L{level_limitation}.v"
# circuits = PrefixCircuit.parse_circuits_from_file(file_path, False)
# circuits[-1].generate_verilog(verilog_path)

file_path = f"ClassicalPCs/{bit_width}bit/SK{bit_width}.log"
verilog_path = f"ClassicalPCs/{bit_width}bit/SK{bit_width}.v"
circuit = PrefixCircuit()
circuit.get_known_init(file_path,bit_width)
circuit.generate_verilog(verilog_path)

