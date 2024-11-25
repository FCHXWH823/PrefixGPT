from openai import OpenAI
import pandas as pd
import csv
import random
from PrefixCircuit import PrefixCircuit
import re

def init_prompt_template_completion(client,model_id,code):
    return client.chat.completions.create(
        model=model_id,
        messages=[
            #{"role": "system", "content": "You are an expert in constructing minimal-area, minimal-delay prefix circuits."},
            {"role": "user", "content": code}
        ],
        # temperature=0.7
    )

def check_prompt_template_completion(client,model_id,code):
    return client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "Please act as a professional verifier of the given prefix circuit."},
            {"role": "user", "content": code}
        ],
        temperature=0.5
    )

def partial_prefix_circuit_prompt(partial_circuit:PrefixCircuit, error_info: str=""):
    circuit = PrefixCircuit()
    circuit.build_ripple_carry_circuit(8)
    kscircuit = PrefixCircuit()
    kscircuit.build_kogge_stone_circuit(8)
    return f'''
    I want to construct a 8-bit prefix circuit. The following are example prefix circuits with corresponding area and delay, where each line represents a node:
    prefix circuit:
    {circuit.print_circuit_info()}
    area:
    {circuit.compute_num_nodes()}
    delay:
    {circuit.compute_overall_delay()}

    Currently give a partial prefix circuit as follows:
    {partialcircuit.print_circuit_info()}
    But it lacks nodes with ranges:
    {partialcircuit.get_missing_ranges()}
    You need to add more prefix nodes to construct these lacked ranges and the final prefix circuit has smaller area or delay than the example prefix circuit. 

    {error_info}

    Add one prefix node following two steps:
    (1) select two existed nodes (two lines) in the partial prefix circuit,
    Conditions:
    value of right_bound in the first line should equal value of left_bound in the second line minus 1.
    (2) derive the range as [left_bound in the first line:right_bound in the second line], and thus left_bound is just left_bound in the first line and right_bound is right_bound in the second line.
    
    Finally, ONLY output the added prefix node in this format:
    node_index: connectedNodes=(xxx, xxx), range=[xxx:xxx], left_bound=xxx, right_bound=xxx
    Note that I hope to construct a prefix circuit different from above examples.
    '''
def circuits_to_str(circuits):
    circuits_str = ""
    for circuit in circuits:
        circuits_str+="prefix circuit:\n"
        circuits_str+=circuit.print_circuit_info()+"\n"
        circuits_str+="area:\n"
        circuits_str+=str(circuit.compute_num_nodes())+"\n"
        circuits_str+="delay:\n"
        circuits_str+=str(circuit.compute_overall_delay())+"\n\n"
    return circuits_str
        

# def partial_prefix_circuit_prompt(existed_circuits, partialcircuit:PrefixCircuit, error_info: str=""):
#     circuit = PrefixCircuit()
#     circuit.build_ripple_carry_circuit(8)
#     kscircuit = PrefixCircuit()
#     kscircuit.build_kogge_stone_circuit(8)
#     return f'''
#     I want to construct a DIFFERENT 8-bit prefix circuit with different area or delay. The following are example prefix circuits with corresponding area and delay, where each line represents a node:
#     {circuits_to_str(existed_circuits)}

#     Currently give a partial prefix circuit and its corresponding area and delay as follows:
#     {partialcircuit.print_circuit_info()}
#     area:
#     {partialcircuit.compute_num_nodes()}
#     delay:
#     {partialcircuit.compute_overall_delay()}
#     But it lacks nodes with ranges:
#     {partialcircuit.get_missing_ranges()}
#     You need to add more prefix nodes to construct these lacked ranges and the final prefix circuit lies on the Pareto frontier in terms of area and delay compared to the example prefix circuits above. 

#     {error_info}

#     Add one prefix node following two steps:
#     (1) select two existed nodes (two lines) in the partial prefix circuit,
#     Conditions:
#     value of right_bound in the first line should equal value of left_bound in the second line minus 1.
#     (2) derive the range as [left_bound in the first line:right_bound in the second line], and thus left_bound is just left_bound in the first line and right_bound is right_bound in the second line.
    
#     Finally, ONLY output the added prefix node in this format:
#     xxx: connectedNodes=(xxx, xxx), range=[xxx:xxx], left_bound=xxx, right_bound=xxx
#     Note that I hope to construct a prefix circuit different from above examples.
#     '''

def partial_prefix_circuit_prompt(existed_circuits, partialcircuit:PrefixCircuit, error_info: str=""):
    circuit = PrefixCircuit()
    circuit.build_ripple_carry_circuit(8)
    kscircuit = PrefixCircuit()
    kscircuit.build_kogge_stone_circuit(8)
    return f'''
    I want to construct a DIFFERENT 8-bit prefix circuit with different area or delay. The following are example prefix circuits with corresponding area and delay, where each line represents a node:
    {circuits_to_str(existed_circuits)}

    Currently give a partial prefix circuit and its corresponding area and delay as follows:
    {partialcircuit.print_circuit_info()}
    area:
    {partialcircuit.compute_num_nodes()}
    delay:
    {partialcircuit.compute_overall_delay()}
    But it lacks nodes with ranges:
    {partialcircuit.get_missing_ranges()}
    You need to add prefix nodes to construct these lacked ranges and the final prefix circuit lies on the Pareto frontier in terms of area and delay compared to the example prefix circuits above. 

    {error_info}

    Adding each prefix node should follow two steps:
    (1) select two existed nodes (two lines) in the partial prefix circuit,
    Conditions:
    value of right_bound in the first line should equal value of left_bound in the second line minus 1.
    (2) derive the range as [left_bound in the first line:right_bound in the second line], and thus left_bound is just left_bound in the first line and right_bound is right_bound in the second line.
    
    Finally, ONLY output each added prefix node and they should be the following format:
    xxx: connectedNodes=(xxx, xxx), range=[xxx:xxx], left_bound=xxx, right_bound=xxx
    '''

# def partial_prefix_circuit_prompt(partial_circuit:PrefixCircuit, error_info: str=""):
#     circuit = PrefixCircuit()
#     circuit.build_ripple_carry_circuit(8)
#     kscircuit = PrefixCircuit()
#     kscircuit.build_kogge_stone_circuit(8)
#     return f'''
#     The following are example generated prefix circuits and their corresponding area and delay are as follows. 
#     prefix circuit:
#     {kscircuit.print_circuit_info()}
#     area:
#     {kscircuit.compute_num_nodes()}
#     delay:
#     {kscircuit.compute_overall_delay()}
#     Each line corresponds to a node in the prefix circuit starting with the node's index in the format:
#     id: connectedNodes=(connect_node_id1, connect_node_id2), range=[left_bound:right_bound]
#     where the connectedNodes represents the connected two nodes' indexs, and the range represents the range of this node, which is the merging of two connected nodes' ranges. For example, about node 10:

#     I want to construct a 8-bit prefix circuit different from the above prefix circuits, which contains nodes with different connectedNodes or range in above example prefix circuits, with smaller area and delay.
#     Currently give a partial prefix circuit as follows:
#     {partialcircuit.print_circuit_info()}
#     But it still lacks nodes with ranges:
#     {partialcircuit.get_missing_ranges()}
#     You need to add more prefix nodes to construct these lacked ranges. 

#     Please note that:
#     {error_info}

#     Currently please add a VALID prefix node to connect two existed nodes in the partial prefix circuit, such as:
#     node_index1: connectedNodes=(n1_connect_node_id1, n1_connect_node_id2), range=[n1_left_bound:n1_right_bound]
#     node_index2: connectedNodes=(n2_connect_node_id1, n2_connect_node_id2), range=[n2_left_bound:n2_right_bound]
#     They should satisfy the following constraint and please double-check: 
#     `n1_right_bound + 1 == n2_left_bound.`
#     Then merge the two connected nodes' ranges and derive the added prefix node's range as [n1_left_bound:n2_right_bound].
#     Finally please ONLY output the added prefix node in the above format.
#     '''

def check_range(circuit: PrefixCircuit, left_node_index: int, right_node_index: int, range):
    left_node_name = f"Node {left_node_index}"
    right_node_name = f"Node {right_node_index}"
    # new added 
    if left_node_name not in circuit.graph.nodes or right_node_name not in circuit.graph.nodes:
        return False
    # Get the ranges of the left and right nodes
    left_range = circuit.graph.nodes[left_node_name]['range']
    right_range = circuit.graph.nodes[right_node_name]['range']

    if left_range[1]+1 != right_range[0]:
        # print("not neighbor ranges!!!")
        return False
    if (left_range[0],right_range[1]) != range:
        # print("not match combined range!!!")
        return False
    return True

# if __name__=='__main__':
    
#     client = OpenAI(
#         api_key=""
#     )
#     model = "o1-mini"

#     kscircuit = PrefixCircuit()
#     kscircuit.build_kogge_stone_circuit(16)

#     circuit = PrefixCircuit()
#     circuit.build_ripple_carry_circuit(16)

#     existed_circuits = [kscircuit]

#     it = 0
#     while (it < 10):
#         partialcircuit = PrefixCircuit()
#         for i in range(16):
#             partialcircuit.add_input_node(i,(i,i))
#         # print(partial_prefix_circuit_prompt([kscircuit], partialcircuit,""))
#         error_info = ""

#         # print(partial_prefix_circuit_prompt(partialcircuit,error_info))

#         while(1):
#             completion = init_prompt_template_completion(client=client,model_id=model,code=partial_prefix_circuit_prompt(existed_circuits,partialcircuit,error_info))
#             prefix_str = completion.choices[0].message.content
#             print(f"The new added prefix node is: {prefix_str}")
#             prefix_str = prefix_str.replace(" ","")
#             match = re.search(r"(\d+):connectedNodes=\((\d+|None),(\d+|None)\),range=\[(\d+):(\d+)\],left_bound=(\d+),right_bound=(\d+)", prefix_str)
#             if not match:
#                 raise ValueError(f"Invalid format in line: {prefix_str}")

#             # Parse extracted parts
#             index = int(match.group(1))
#             left_node = None if match.group(2) == "None" else int(match.group(2))
#             right_node = None if match.group(3) == "None" else int(match.group(3))
#             connected_nodes = (left_node, right_node)
#             bit_range = (int(match.group(4)), int(match.group(5)))
#             left_bound = int(match.group(6))
#             right_bound = int(match.group(7))

#             if check_range(partialcircuit,left_node,right_node,bit_range) and not partialcircuit.get_repeated_info(bit_range):
#                 partialcircuit.add_prefix_node(left_node,right_node,index)
#                 error_info = ""
#                 print(f"The new partial prefix circuit is:\n{partialcircuit.print_circuit_info()}")
#                 if not len(partialcircuit.get_missing_ranges()):
#                     break
#             elif partialcircuit.get_repeated_info(bit_range):
#                 error_info += f"This is a prefix node existed in current prefix circuit: connectedNodes=({left_node},{right_node}), range=({bit_range[0]},{bit_range[1]}), left_bound={left_bound}, right_bound={right_bound}. Do not add it!"
#             else:
#                 error_info += f"Can not connect {left_node}, {right_node}!!!"
#         print(f"===============================Generate a full prefix circuit: area={partialcircuit.compute_num_nodes()}, delay={partialcircuit.compute_overall_delay()}=============================")
#         existed_circuits.append(partialcircuit)
#         existed_circuits = PrefixCircuit.non_dominated_sort(existed_circuits)
#         it += 1
        
if __name__=='__main__':
    
    client = OpenAI(
        api_key=""
    )
    model = "o1-mini"

    kscircuit = PrefixCircuit()
    kscircuit.build_kogge_stone_circuit(16)

    circuit = PrefixCircuit()
    circuit.build_ripple_carry_circuit(16)

    existed_circuits = [kscircuit]

    it = 0
    while (it < 20):
        partialcircuit = PrefixCircuit()
        for i in range(16):
            partialcircuit.add_input_node(i,(i,i))
        print(partial_prefix_circuit_prompt([kscircuit], partialcircuit,""))
        error_info = ""

        # print(partial_prefix_circuit_prompt(partialcircuit,error_info))

        while(1):
            completion = init_prompt_template_completion(client=client,model_id=model,code=partial_prefix_circuit_prompt(existed_circuits,partialcircuit,error_info))
            prefix_str = completion.choices[0].message.content
            prefix_str = prefix_str.replace(" ","")
            print(f"The new added prefix node is: {prefix_str}")
            prefix_lines = prefix_str.split('\n')
            for prefix_line in prefix_lines:
                match = re.search(r"(\d+):connectedNodes=\((\d+|None),(\d+|None)\),range=\[(\d+):(\d+)\],left_bound=(\d+),right_bound=(\d+)", prefix_line)
                if not match:
                    continue
                # Parse extracted parts
                index = int(match.group(1))
                left_node = None if match.group(2) == "None" else int(match.group(2))
                right_node = None if match.group(3) == "None" else int(match.group(3))
                connected_nodes = (left_node, right_node)
                bit_range = (int(match.group(4)), int(match.group(5)))
                left_bound = int(match.group(6))
                right_bound = int(match.group(7))

                if check_range(partialcircuit,left_node,right_node,bit_range) and not partialcircuit.get_repeated_info(bit_range):
                    partialcircuit.add_prefix_node(left_node,right_node,partialcircuit.compute_num_nodes())
                    # print(f"The new partial prefix circuit is:\n{partialcircuit.print_circuit_info()}")
                    if not len(partialcircuit.get_missing_ranges()):
                        break
                elif partialcircuit.get_repeated_info(bit_range):
                    error_info += f"This is a prefix node existed in current prefix circuit: connectedNodes=({left_node},{right_node}), range=({bit_range[0]},{bit_range[1]}), left_bound={left_bound}, right_bound={right_bound}. Do not add it!"
                else:
                    error_info += f"Can not connect {left_node}, {right_node}!!!"
            if not len(partialcircuit.get_missing_ranges()):
                        break
        print(f"===============================Generate a full prefix circuit: area={partialcircuit.compute_num_nodes()}, delay={partialcircuit.compute_overall_delay()}=============================")
        existed_circuits.append(partialcircuit)
        existed_circuits = PrefixCircuit.non_dominated_sort(existed_circuits)
        with open("GPTPrefix16.txt", "w") as file:
            file.write(circuits_to_str(existed_circuits))
        it += 1
        






