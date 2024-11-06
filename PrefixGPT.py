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
            {"role": "system", "content": "Please act as a professional hardware designer for co-optimizing the area and delay of the prefix circuit."},
            {"role": "user", "content": code}
        ],
        temperature=0.5
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

if __name__=='__main__':
    # Example usage:
    input_string = """
    The current circuit computes:
    - [0:0], [0:1], [0:3], [0:7]

    ### Missing Prefix Sums
    - [0:2], [0:4], [0:5], [0:6]

    ### Adding Missing Nodes
    - **Node 15**: Connects (1, 2) with range [0:2].
    - **Node 16**: Connects (12, 10) with range [0:5].
    - **Node 17**: Connects (16, 11) with range [0:6].

    ### Updated Prefix Circuit
    prefix circuit:
    0: connectedNodes=(None, None), range=[0:0].
    1: connectedNodes=(None, None), range=[1:1].
    2: connectedNodes=(None, None), range=[2:2].
    3: connectedNodes=(None, None), range=[3:3].
    4: connectedNodes=(None, None), range=[4:4].
    5: connectedNodes=(None, None), range=[5:5].
    6: connectedNodes=(None, None), range=[6:6].
    7: connectedNodes=(None, None), range=[7:7].
    8: connectedNodes=(0, 1), range=[0:1].
    9: connectedNodes=(2, 3), range=[2:3].
    10: connectedNodes=(4, 5), range=[4:5].
    11: connectedNodes=(6, 7), range=[6:7].
    12: connectedNodes=(8, 9), range=[0:3].
    13: connectedNodes=(10, 11), range=[4:7].
    14: connectedNodes=(12, 13), range=[0:7].
    15: connectedNodes=(1, 2), range=[0:2].
    16: connectedNodes=(12, 10), range=[0:5].
    17: connectedNodes=(16, 11), range=[0:6].
    area:
    0
    delay:
    2
    """

    # # Parse and initialize the prefix circuit
    # lines = input_string.split('\n')
    # prefixLines = []
    # for line in lines:
    #     if 'connectedNodes' in line and 'range' in line:
    #         prefixLines.append(line)
    # prefixString = '\n'.join(prefixLines)

    # circuit = PrefixCircuit()
    # circuit.construct_circuit_from_info_string(prefixString)
    # print(circuit.print_circuit_info())
    # if circuit.check_circuit_integrity():
    #     print("This prefix circuit is valid")
    # else:
    #     print("This prefix circuit is invalid")


    client = OpenAI(
        api_key=""
    )
    model = "gpt-3.5-turbo"
    circuit = PrefixCircuit()
    circuit.build_ripple_carry_circuit(8)
    kscircuit = PrefixCircuit()
    kscircuit.build_kogge_stone_circuit(8)
    Init_prompt = f'''
    I have some example prefix circuits and their corresponding area and delay as follows. 
    prefix circuit:
    {circuit.print_circuit_info()}
    area:
    {circuit.compute_num_nodes()}
    delay:
    {circuit.compute_overall_delay()}

    prefix circuit:
    {kscircuit.print_circuit_info()}
    area:
    {kscircuit.compute_num_nodes()}
    delay:
    {kscircuit.compute_overall_delay()}
    Please give me a new prefix circuit, which should satisfy four constraints: (1) it must contain 7 nodes with range=[0:x]; (2) prefix node's range matches the combination of two connected nodes' ranges; For example, a node connects two nodes with range [2:4] and [5:7] and its range will become [2:7]. (3) prefix node connects two nodes with neighbor ranges; For exmaple, a node connecting two nodes with range [2:4] and [6:7] is not allowable. I hope it has at least one smaller property, i.e., area or delay, than each of the example prefix circuits above. It
    Please ONLY output the prefix circuit with the same format:
    prefix circuit:
    xxx
    '''

    Init_check_prompt = f'''
    I have some prefix circuits and their corresponding area and delay as follows. 
    prefix circuit:
    {circuit.print_circuit_info()}
    area:
    {circuit.compute_num_nodes()}
    delay:
    {circuit.compute_overall_delay()}

    prefix circuit:
    {kscircuit.print_circuit_info()}
    area:
    {kscircuit.compute_num_nodes()}
    delay:
    {kscircuit.compute_overall_delay()}
    '''

    generation_prompt = Init_prompt
    for _ in range(50):
        completion = init_prompt_template_completion(client=client,model_id=model,code=generation_prompt)
        prefix_str = completion.choices[0].message.content
        print(prefix_str)
        circuit = None
        while (1):
            lines = prefix_str.split('\n')
            prefixLines = []
            for line in lines:
                if 'connectedNodes' in line and 'range' in line:
                    prefixLines.append(line)
            prefixString = '\n'.join(prefixLines)
            circuit = PrefixCircuit()
            circuit.construct_circuit_from_info_string(prefixString)
            if circuit.check_circuit_integrity():
                break

            check_prompt = f'''
            Given such a prefix circuit:
            {prefixString}
            Please check three things: (1) prefix node's range does not match the combination of two connected nodes' ranges; (2) prefix node connects two nodes with non-neighbor ranges; (3) it lacks nodes with one of the 7 ranges [0:x].
            Please remove invalid prefix nodes while remain other valid prefix nodes and add USEFUL prefix nodes to compute all [0:0], [0:1], [0:2],...,[0:7] different from above example prefix circuits, but also with purpose to co-minimize the area and delay. 
            Please output your generated valid prefix circuit with the same format.
            '''
            check_prompt = Init_check_prompt+"\n\n"+check_prompt
            check_completion = check_prompt_template_completion(client=client,model_id=model,code=check_prompt)
            prefix_str = check_completion.choices[0].message.content
            print(check_completion.choices[0].message.content)
        
        #update generation prompt
        generation_prompt = generation_prompt +"\n\nprefix circuit:\n"+circuit.print_circuit_info()+"\narea:\n"+str(circuit.compute_num_nodes())+"\ndelay:\n"+str(circuit.compute_overall_delay())+"\n"
        Init_check_prompt += "\n\nprefix circuit:\n"+circuit.print_circuit_info()+"\narea:\n"+str(circuit.compute_num_nodes())+"\ndelay:\n"+str(circuit.compute_overall_delay())+"\n"
        
        






