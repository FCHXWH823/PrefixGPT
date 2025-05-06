from openai import OpenAI
import pandas as pd
import csv
import random
from PrefixCircuit import PrefixCircuit
import re
import os
import yaml
import time

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
def circuits_to_str(circuits, level_bound):
    circuits_str = f"The following are some prefix circuits under level bound {level_bound} with corresponding area, where each line represents a node:\n"
    if not len(circuits):
        circuits_str += "No example prefix circuits."
    for circuit in circuits:
        circuits_str+="prefix circuit:\n"
        circuits_str+=circuit.print_circuit_info()+"\n"
        circuits_str+="area:\n"
        circuits_str+=str(circuit.compute_num_nodes())+"\n"
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

def partial_prefix_circuit_prompt(bit_width, existed_circuits, partialcircuit:PrefixCircuit, level_bound:int, error_info: str=""):
    circuit = PrefixCircuit()
    circuit.build_ripple_carry_circuit(8)
    kscircuit = PrefixCircuit()
    kscircuit.build_kogge_stone_circuit(8)
    return f'''
    I want to construct a {bit_width}-bit prefix circuit with minimized area, but with level bound {level_bound}, i.e., each node's level should be no larger than {level_bound}. 
    
    {circuits_to_str(existed_circuits,level_bound)}

    Currently give a partial prefix circuit and its corresponding area as follows:
    {partialcircuit.print_circuit_info()}
    area:
    {partialcircuit.compute_num_nodes()}
    But it lacks nodes with ranges:
    {partialcircuit.get_missing_ranges()}
    You need to add prefix nodes to construct these lacked ranges, but the final prefix circuit should have smaller area compared to the above prefix circuits. 

    {error_info}

    Adding each prefix node should follow two steps:
    (1) select two existed nodes (two lines) in the partial prefix circuit,
    Conditions:
    value of right_bound in the first line should equal value of left_bound in the second line minus 1.
    (2) derive the range as [left_bound in the first line:right_bound in the second line], and thus left_bound is just left_bound in the first line and right_bound is right_bound in the second line.
    (3) derive the level as the larger level in the two lines plus 1.
    
    Finally, ONLY output each added prefix node and they should be the following format:
    xxx: connectedNodes=(xxx, xxx), range=[xxx:xxx], left_bound=xxx, right_bound=xxx, level=xxx
    '''


def Modified_partial_prefix_circuit_prompt(bit_width, existed_circuits, partialcircuit:PrefixCircuit, level_bound:int, error_info: str=""):
    circuit = PrefixCircuit()
    circuit.build_ripple_carry_circuit(8)
    kscircuit = PrefixCircuit()
    kscircuit.build_kogge_stone_circuit(8)
    missing_ranges = partialcircuit.get_missing_ranges()
    # if len(missing_ranges) > 8:
    #     missing_ranges = missing_ranges[:8]
    return f'''
    I want to construct a {bit_width}-bit prefix circuit with minimized area, but with level bound {level_bound}, i.e., each node's level should be no larger than {level_bound}. 
    
    {circuits_to_str(existed_circuits,level_bound)}

    Currently give a partial prefix circuit and its corresponding area as follows:
    {partialcircuit.print_circuit_info()}
    area:
    {partialcircuit.compute_num_nodes()}
    But it lacks nodes with ranges:
    {missing_ranges}
    You do not need to directly compute all the missing ranges. Instead, try to add prefix nodes that connect existing nodes in the current partial prefix circuit and their corresponding ranges can serve as useful sub-ranges for constructing the missing ranges in future steps. 
    The final prefix circuit should have a smaller area than any of the above example prefix circuits.
    Try to propose new prefix node connections to help reduce area.

    {error_info}

    Adding each prefix node should follow three steps:
    (1) Select two existing nodes (two lines) that are already present in the current partial prefix circuit. 
    The indices of the selected nodes must match one of the following valid candidate pairs:
    {partialcircuit.get_pruned_candidate_prefix_pairs(level_bound)}

    (2) derive the range as [left_bound:right_bound], where left_bound is the left bound of the first node and right_bound is the right bound of the second node.

    (3) derive the level as max(level of the two nodes) + 1.
    
    Finally, ONLY output each added prefix node without any extra explanation, and follow the exact format:
    xxx: connectedNodes=(xxx, xxx), range=[xxx:xxx], left_bound=xxx, right_bound=xxx, level=xxx
    '''

# def Modified_partial_prefix_circuit_prompt(bit_width, existed_circuits, partialcircuit:PrefixCircuit, level_bound:int, error_info: str=""):
#     circuit = PrefixCircuit()
#     circuit.build_ripple_carry_circuit(8)
#     kscircuit = PrefixCircuit()
#     kscircuit.build_kogge_stone_circuit(8)
#     missing_ranges = partialcircuit.get_missing_ranges()
#     # if len(missing_ranges) > 8:
#     #     missing_ranges = missing_ranges[:8]
#     return f'''
#     I want to construct a {bit_width}-bit prefix circuit with minimized area, but with level bound {level_bound}, i.e., each node's level should be no larger than {level_bound}. 
    
#     {circuits_to_str(existed_circuits,level_bound)}

#     Currently give a partial prefix circuit and its corresponding area as follows:
#     {partialcircuit.print_circuit_info()}
#     area:
#     {partialcircuit.compute_num_nodes()}
#     But it lacks nodes with ranges:
#     {missing_ranges}
#     You need to add prefix nodes to construct these lacked ranges.
#     For exmaple, the range [0:3] can be constructed by adding a prefix node with range [0:1] and a prefix node with range [2:3].
#     The final prefix circuit should have a smaller area than any of the above example prefix circuits.
#     Try to propose new prefix node connections to help reduce area.

#     {error_info}

#     Adding each prefix node should follow three steps:
#     (1) Select two existing nodes (two lines) that are already present in the current partial prefix circuit. 
#     The indices of the selected nodes must match one of the following valid candidate pairs:
#     {partialcircuit.get_pruned_candidate_prefix_pairs(level_bound)}

#     (2) derive the range as [left_bound:right_bound], where left_bound is the left bound of the first node and right_bound is the right bound of the second node.

#     (3) derive the level as max(level of the two nodes) + 1.
    
#     Finally, ONLY output each added prefix node without any extra explanation, and follow the exact format:
#     xxx: connectedNodes=(xxx, xxx), range=[xxx:xxx], left_bound=xxx, right_bound=xxx, level=xxx
#     '''

# def Modified_partial_prefix_circuit_prompt(bit_width, existed_circuits, partialcircuit:PrefixCircuit, level_bound:int, error_info: str=""):
#     circuit = PrefixCircuit()
#     circuit.build_ripple_carry_circuit(8)
#     kscircuit = PrefixCircuit()
#     kscircuit.build_kogge_stone_circuit(8)
#     return f'''
#     I want to construct a {bit_width}-bit prefix circuit with minimized area. 
    
#     {circuits_to_str(existed_circuits,level_bound)}

#     Currently give a partial prefix circuit and its corresponding area as follows:
#     {partialcircuit.print_circuit_info()}
#     area:
#     {partialcircuit.compute_num_nodes()}
#     But it lacks nodes with ranges:
#     {partialcircuit.get_missing_ranges()}
#     The final prefix circuit should have a smaller area than any of the above example prefix circuits.
#     Try to propose new prefix node connections to help reduce area.

#     {error_info}

#     Adding each prefix node should follow three steps:
#     (1) Select exactly one pair of existing nodes from the following list of valid candidate pairs:
#     {partialcircuit.get_pruned_candidate_prefix_pairs(level_bound)}
#     Only choose from this list. Do not invent, assume, or construct any other combinations. These candidate pairs are pre-validated to be structurally and logically correct within the current circuit.

#     (2) derive the range as [left_bound:right_bound], where left_bound is from the first node and right_bound is from the second node.

#     (3) derive the level as max(level of the two nodes) + 1.
    
#     Finally, ONLY output each added prefix node without any extra explanation, and follow the exact format:
#     xxx: connectedNodes=(xxx, xxx), range=[xxx:xxx], left_bound=xxx, right_bound=xxx, level=xxx
#     '''

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

def check_level(circuit: PrefixCircuit, left_node_index: int, right_node_index: int, level_bound: int):

    left_node_name = f"Node {left_node_index}"
    right_node_name = f"Node {right_node_index}"

    # Get the ranges of the left and right nodes
    left_range = circuit.graph.nodes[left_node_name]['range']
    if left_range[0] == 0:
        lb = level_bound
    else:
        lb = level_bound - 1

    # new added 
    if left_node_name not in circuit.graph.nodes or right_node_name not in circuit.graph.nodes:
        return False
    level_current = max(circuit.graph.nodes[left_node_name]['level'],circuit.graph.nodes[right_node_name]['level'])+1
    if level_current <= lb:
        return True
    else:
        return False

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

def get_init_designs(dir, bit_width):
    kscircuit = PrefixCircuit()
    # kscircuit.build_ripple_carry_circuit(bit_width)
    kscircuit.build_kogge_stone_circuit(bit_width)
    if not os.path.exists(dir):
        return [kscircuit], [kscircuit],0
    else:
        existed_circuits = []
        trunc_existed_circuits = []
        iterations = []
        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            if 'it' in filename:
                iterations.append(int(filename.split('.')[0].split('_')[-1].replace("it","")))
                existed_circuits += PrefixCircuit.parse_circuits_from_file(file_path, False)
        existed_circuits = PrefixCircuit.sort_circuits_by_area(existed_circuits)
        if len(existed_circuits) >= 10:
            trunc_existed_circuits = existed_circuits[-10:]
        else:
            trunc_existed_circuits = existed_circuits
        return existed_circuits, trunc_existed_circuits,max(iterations)+1

def prune_useless_nodes(dir, bit_width, level_limit):
    if os.path.exists(dir):
        existed_circuits = []
        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            if 'it' in filename:
                existed_circuits += PrefixCircuit.parse_circuits_from_file(file_path)
        existed_circuits = PrefixCircuit.sort_circuits_by_area(existed_circuits)
        with open(f"./GPTPrefix{bit_width}_L{level_limit}_{model}_Pruned_{USE_HUMAN_HEURISTIC}/GPTPrefix{bit_width}_L{level_limit}_{model}_Pruned_{USE_HUMAN_HEURISTIC}_Pruned.txt", "w") as file:
            file.write(circuits_to_str(existed_circuits,level_limit))


if __name__=='__main__':
    with open("Config.yml") as file:
        config = yaml.safe_load(file)

    # client = OpenAI(
    #     api_key= config["Openai_API_Key"]
    # )
    
    model = config["Model_Name"]
    if "o" in model or "gpt" in model:
        client = OpenAI(
            api_key= config["Openai_API_Key"]
        )
    elif "deepseek" in model:
        client = OpenAI(
            api_key= config["DeepSeek_API_Key"],
            base_url="https://api.deepseek.com",
        )
    level_limit = config["Level"]
    bit_width = config["BitWidth"]

    spcr_iteration_bound = config["Spcr_It_Bound"]
    dse_iteration_bound = config["Dse_It_Bound"]
    USE_HUMAN_HEURISTIC = config["USE_HUMAN_HEURISTIC"]

    kscircuit = PrefixCircuit()
    kscircuit.build_kogge_stone_circuit(bit_width)
    print(kscircuit.print_circuit_info())

    circuit = PrefixCircuit()
    circuit.build_ripple_carry_circuit(bit_width)

    # existed_circuits = [kscircuit]
    # trunc_existed_circuits = [kscircuit]
    # prune_useless_nodes(f"GPTPrefix{bit_width}_L{level_limit}",bit_width,level_limit)
    existed_circuits, trunc_existed_circuits,max_iteration = get_init_designs(f"GPTPrefix{bit_width}_L{level_limit}_{model}_Pruned_{USE_HUMAN_HEURISTIC}",bit_width)
    

    if not os.path.exists(f"GPTPrefix{bit_width}_L{level_limit}_{model}_Pruned_{USE_HUMAN_HEURISTIC}"):
        os.makedirs(f"GPTPrefix{bit_width}_L{level_limit}_{model}_Pruned_{USE_HUMAN_HEURISTIC}")
        

    it = max_iteration
    while (it < dse_iteration_bound):
        partialcircuit = PrefixCircuit()
        for i in range(bit_width):
            partialcircuit.add_input_node(i,(i,i))
        # print(partial_prefix_circuit_prompt([kscircuit], partialcircuit,level_limit,""))
        

        # print(partial_prefix_circuit_prompt(partialcircuit,error_info))
        it_in = 0
        it_in_limit_flag = 0
        # record the runtime
        start_time = time.time()
        while(1):
            error_info = ""
            if not USE_HUMAN_HEURISTIC:
                prompt = partial_prefix_circuit_prompt(bit_width,trunc_existed_circuits,partialcircuit,level_limit,error_info)
            else:
                prompt = Modified_partial_prefix_circuit_prompt(bit_width,trunc_existed_circuits,partialcircuit,level_limit,error_info)
            completion = init_prompt_template_completion(client=client,model_id=model,code=prompt)
            prefix_str = completion.choices[0].message.content
            prefix_str = prefix_str.replace(" ","")
            # print(f"The new added prefix node is: {prefix_str}")
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

                if check_range(partialcircuit,left_node,right_node,bit_range) and not partialcircuit.get_repeated_info(bit_range) and check_level(partialcircuit,left_node,right_node,level_limit):
                # if check_range(partialcircuit,left_node,right_node,bit_range) and check_level(partialcircuit,left_node,right_node,level_limit):
                    partialcircuit.add_prefix_node(left_node,right_node,partialcircuit.compute_num_nodes())
                    # print(f"The new partial prefix circuit is:\n{partialcircuit.print_circuit_info()}")
                    if not len(partialcircuit.get_missing_ranges()):
                        break
                elif partialcircuit.get_repeated_info(bit_range):
                    error_info += f"This is a prefix node with connectedNodes=({left_node},{right_node}) existed in current prefix circuit. Do not add it!\n"
                elif not check_range(partialcircuit,left_node,right_node,bit_range):
                    error_info += f"Can not connect {left_node}, {right_node}!!!\n"
                elif not check_level(partialcircuit,left_node,right_node,level_limit):
                    error_info += f"This is a prefix node connectedNodes=({left_node},{right_node}) exceeding level bound {level_limit}. Do not add it\n"
            # partialcircuit.prune_duplicate_ranges()
            # partialcircuit.add_nodes_for_missing_ranges(level_limit)
            lacked_ranges = partialcircuit.get_missing_ranges()
            print(f"=============it{it} it_in{it_in}: {len(lacked_ranges)}=====================")
            if not len(lacked_ranges):
                break
            it_in += 1
            if it_in > spcr_iteration_bound:
                it_in_limit_flag = 1
                break
        end_time = time.time()
        if not it_in_limit_flag:
            partialcircuit.remove_useless_nodes()
            if USE_HUMAN_HEURISTIC:
                num_nodes = partialcircuit.compute_num_nodes()
                next_num_nodes = 0
                while next_num_nodes < num_nodes:
                    num_nodes = partialcircuit.compute_num_nodes()
                    optimized_pc_nodes = partialcircuit.optimize_fanout_singletons(level_limit)
                    partialcircuit.remove_useless_nodes()
                    next_num_nodes = partialcircuit.compute_num_nodes()
            print(f"===============================it{it}=> Generate a full prefix circuit: area={partialcircuit.compute_num_nodes()}, delay={partialcircuit.compute_overall_delay()}=============================")
            print(f"# Use {it_in} iterations and {end_time - start_time:.4f}s to generate a full prefix circuit")
            with open(f"./GPTPrefix{bit_width}_L{level_limit}_{model}_Pruned_{USE_HUMAN_HEURISTIC}/GPTPrefix{bit_width}_L{level_limit}_{model}_Pruned_{USE_HUMAN_HEURISTIC}_TrajectoryTrunc_it{it}.txt", "w") as file:
                file.write(f"# Use {it_in} iterations and {end_time - start_time:.4f}s to generate a full prefix circuit")    
                file.write(circuits_to_str([partialcircuit],level_limit))
            existed_circuits.append(partialcircuit)
            if len(existed_circuits) >= 5:
                trunc_existed_circuits = PrefixCircuit.sort_circuits_by_area(existed_circuits)[-5:]
            else:
                trunc_existed_circuits = PrefixCircuit.sort_circuits_by_area(existed_circuits)
        it += 1
    
    with open(f"./GPTPrefix{bit_width}_L{level_limit}_{model}_Pruned_{USE_HUMAN_HEURISTIC}/GPTPrefix{bit_width}_L{level_limit}_{model}_Pruned_{USE_HUMAN_HEURISTIC}_TrajectoryTrunc.txt", "w") as file:
            file.write(circuits_to_str(existed_circuits,level_limit))
    prune_useless_nodes(f"GPTPrefix{bit_width}_L{level_limit}_{model}_Pruned_{USE_HUMAN_HEURISTIC}",bit_width,level_limit)
        






