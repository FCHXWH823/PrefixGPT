import networkx as nx
import matplotlib.pyplot as plt

import networkx as nx
import matplotlib.pyplot as plt
import math
import re
import random
import nxpd
import numpy as np

class PrefixCircuit:
    def __init__(self):
        # Initialize a directed graph to represent the circuit
        self.graph = nx.DiGraph()
        self.node_counter = 0  # Keeps track of node indices
        self.output_nodes = []  # List to store output nodes computing [i:0] ranges

    def add_input_node(self, index, bit_range):
        """
        Adds an input node representing an initial propagate and generate signal.

        Parameters:
            index (int): Unique identifier for the node.
            bit_range (tuple): Tuple containing (start_index, end_index).
        """
        node_name = f"Node {index}"
        self.graph.add_node(node_name, index=index, range=bit_range, type='input', level=1)

    def add_prefix_node(self, left_node_index, right_node_index, index):
        """
        Adds a prefix node that combines two nodes corresponding to adjacent slices of bits.

        Parameters:
            left_node_index (int): Index of the left input node.
            right_node_index (int): Index of the right input node.
            index (int): Unique identifier for the new prefix node.
        """
        node_name = f"Node {index}"
        left_node_name = f"Node {left_node_index}"
        right_node_name = f"Node {right_node_index}"

        # Check if the input nodes exist
        if left_node_name not in self.graph or right_node_name not in self.graph:
            raise ValueError("One or both input nodes do not exist.")

        # Get the ranges of the left and right nodes
        left_range = self.graph.nodes[left_node_name]['range']
        right_range = self.graph.nodes[right_node_name]['range']

        # Ensure the ranges are adjacent and properly ordered
        # For example, left_range = (start, mid), right_range = (mid+1, end)
        if left_range[1] + 1 != right_range[0]:
            raise ValueError("The ranges of the left and right nodes are not adjacent.")

        # Compute the combined range
        combined_range = (left_range[0], right_range[1])

        # Compute the level
        level_left = self.graph.nodes[left_node_name]['level']
        level_right = self.graph.nodes[right_node_name]['level']
        level_current = max(level_left,level_right)+1

        # Add the new prefix node
        self.graph.add_node(node_name, index=index, range=combined_range, type='prefix',level = level_current)
        # Add edges from the input nodes to the new prefix node
        self.graph.add_edge(left_node_name, node_name)
        self.graph.add_edge(right_node_name, node_name)

        # Check if the combined range is [i:0]
        if combined_range[0] == 0:
            self.output_nodes.append(node_name)

    def remove_prefix_node(self, index):
        """
        Removes a prefix node from the circuit.

        Parameters:
            index (int): Unique identifier of the prefix node to remove.
        """
        node_name = f"Node {index}"
        if node_name in self.graph:
            # Remove the node and its associated edges
            self.graph.remove_node(node_name)
            # Remove from output_nodes if present
            if node_name in self.output_nodes:
                self.output_nodes.remove(node_name)
        else:
            print(f"Node {index} does not exist in the circuit.")

    def get_node_levels(self):
        """
        Computes and returns the level of each node in the circuit.

        Returns:
            levels (dict): A dictionary mapping node names to their levels.
        """
        levels = {}
        # Initialize levels for input nodes
        for node, data in self.graph.nodes(data=True):
            if data['type'] == 'input':
                levels[node] = 1 # change initial level to 1

        # Assign levels to prefix nodes
        nodes_to_process = [node for node in self.graph.nodes if node not in levels]
        while nodes_to_process:
            for node in nodes_to_process[:]:
                preds = list(self.graph.predecessors(node))
                if all(pred in levels for pred in preds):
                    # Level is one more than max level of predecessors
                    level = max(levels[pred] for pred in preds) + 1
                    levels[node] = level
                    nodes_to_process.remove(node)

        return levels

    def visualize(self):
        """
        Visualizes the prefix circuit using NetworkX and Matplotlib.
        Arranges input nodes at the top and internal nodes below.
        """
        levels = self.get_node_levels()

        # Group nodes by levels
        level_nodes = {}
        max_level = max(levels.values())
        for node, level in levels.items():
            if level not in level_nodes:
                level_nodes[level] = []
            level_nodes[level].append(node)

        # Assign positions
        pos = {}
        y_gap = 1  # Vertical gap between levels
        x_gap = 1  # Horizontal gap between nodes

        for level in range(max_level + 1):
            nodes = level_nodes.get(level, [])
            num_nodes = len(nodes)
            x_positions = [i * x_gap - (num_nodes - 1) * x_gap / 2 for i in range(num_nodes)]
            y_position = -level * y_gap  # Negative to have inputs at the top

            for i, node in enumerate(nodes):
                pos[node] = (x_positions[i], y_position)

        # Prepare labels and colors
        labels = {}
        node_colors = []
        node_shapes = []
        for node, data in self.graph.nodes(data=True):
            bit_range = data['range']
            range_str = f"[{bit_range[0]}:{bit_range[1]}]"
            node_level = levels[node]
            labels[node] = f"{node}\nRange: {range_str}\nLevel: {node_level}"

            if data['type'] == 'input':
                node_colors.append('skyblue')
                node_shapes.append('o')
            elif node in self.output_nodes:
                node_colors.append('lightgreen')  # Highlight output nodes
                node_shapes.append('o')
            else:
                node_colors.append('lightgreen')
                node_shapes.append('o')

        plt.figure(figsize=(12, 6))
        nx.draw(self.graph, pos, labels=labels, node_color=node_colors, with_labels=True, arrows=True, node_size=2000)
        plt.title("Prefix Circuit")
        plt.axis('off')
        plt.show()
        plt.savefig('prefix.png')
    
    def build_ripple_carry_circuit(self, num_bits):
        """
        Builds a ripple-carry prefix circuit for the specified number of bits.

        Parameters:
            num_bits (int): The number of bits for the adder.
        """
        # Clear existing graph
        self.graph.clear()
        self.output_nodes = []

        # Add input nodes
        for i in range(num_bits):
            self.add_input_node(index=i, bit_range=(i, i))

        # Build the ripple-carry circuit
        current_node_index = num_bits  # Start indexing prefix nodes after input nodes
        for i in range(1, num_bits):
            left_index = current_node_index - 1 if i > 1 else i - 1
            right_index = i
            self.add_prefix_node(
                left_node_index=left_index,
                right_node_index=right_index,
                index=current_node_index
            )
            current_node_index += 1
    
    def build_kogge_stone_circuit(self, num_bits):
        """
        Builds a Kogge-Stone prefix circuit for the specified number of bits.
        """
        # Clear existing graph
        self.graph.clear()
        self.output_nodes = []

        # Add input nodes
        for i in range(num_bits):
            self.add_input_node(index=i, bit_range=(i, i))

        # Build the Kogge-Stone circuit
        levels = int(math.ceil(math.log2(num_bits)))
        node_indices = {}  # Dictionary to keep track of nodes at each bit position and level

        # Initialize node indices with input nodes
        for i in range(num_bits):
            node_indices[(1, i)] = i  # (length of range, position): node_index

        current_node_index = num_bits  # Start indexing prefix nodes after input nodes

        # Build each level
        for level in range(1, levels + 1):
            stride = 1<<level
            stride_last_level = 1<<(level-1)
            for i in range(num_bits):
                if i >= stride_last_level:
                    rsb_position = i
                    lsb_position = i-stride+1 if i-stride+1 >=0 else 0
                    im_position = i-stride_last_level+1
                    right_node_index = node_indices[(stride_last_level,i)]
                    left_node_index = node_indices[(im_position-lsb_position,im_position-1)]

                    self.add_prefix_node(
                        left_node_index=left_node_index,
                        right_node_index=right_node_index,
                        index=current_node_index
                    )
                    node_indices[(rsb_position-lsb_position+1,rsb_position)] = current_node_index
                    current_node_index += 1

    def print_circuit_info(self):
        """
        Prints and returns the information of the current prefix circuit.
        Each line contains a node's index, connected nodes' indices, and range in the format:
        'index: connectedNodes=(i,j), range=[k:l].'
        """
        output_lines = []
        # print("Circuit Nodes Information:")
        for node in self.graph.nodes:
            data = self.graph.nodes[node]
            index = data['index']
            bit_range = data['range']

            # Get predecessors' indices
            predecessors = list(self.graph.predecessors(node))
            pred_indices = [self.graph.nodes[pred]['index'] for pred in predecessors]

            # Ensure we have exactly two predecessors for formatting
            if len(pred_indices) == 0:
                connected_nodes = (None, None)
            elif len(pred_indices) == 1:
                connected_nodes = (pred_indices[0], None)
            else:
                connected_nodes = tuple(pred_indices[:2])  # Take only the first two if more

            # Format range as [k:l]
            range_str = f"[{bit_range[0]}:{bit_range[1]}]"

            # Prepare the output line
            line = f"{index}: connectedNodes={connected_nodes}, range={range_str}, left_bound={bit_range[0]}, right_bound={bit_range[1]}, level={data['level']}."
            # print(line)
            output_lines.append(line)

        # Return the combined output string
        return '\n'.join(output_lines)

    def construct_circuit_from_info_string(self, info_string):
        """
        Constructs the circuit from a string containing node information in the format:
        'index: connectedNodes=(i,j), range=[k:l].'
        """
        # Clear existing graph and output nodes list
        self.graph.clear()
        self.output_nodes = []

        # Split the string into lines and parse each line
        lines = info_string.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Remove the trailing dot if it exists
            if line.endswith('.'):
                line = line[:-1]

            # Extract index, connected nodes, and range using regex for more precision
            match = re.match(r"(\d+): connectedNodes=\((\d+|None), (\d+|None)\), range=\[(\d+):(\d+)\]", line)
            if not match:
                raise ValueError(f"Invalid format in line: {line}")

            # Parse extracted parts
            index = int(match.group(1))
            left_node = None if match.group(2) == "None" else int(match.group(2))
            right_node = None if match.group(3) == "None" else int(match.group(3))
            connected_nodes = (left_node, right_node)
            bit_range = (int(match.group(4)), int(match.group(5)))

            # Determine node type and add to the graph
            node_name = f"Node {index}"
            if left_node is None and right_node is None:
                # This is an input node
                self.add_input_node(index,bit_range)
                # self.graph.add_node(node_name, index=index, range=bit_range, type='input')
            else:
                # This is a prefix node
                self.add_prefix_node(left_node,right_node,index)
                # self.graph.add_node(node_name, index=index, range=bit_range, type='prefix')
                # Add edges from each connected node, if they exist
                if left_node is not None:
                    self.graph.add_edge(f"Node {left_node}", node_name)
                if right_node is not None:
                    self.graph.add_edge(f"Node {right_node}", node_name)

            # Check if this node should be an output node
            if bit_range[0] == 0 and connected_nodes != (None, None):
                self.output_nodes.append(node_name)
       
    def compute_overall_delay(self):
        """
        Computes and returns the overall delay of the prefix circuit.
        The delay is determined by the longest path from any input node to any output node.
        Returns:
            overall_delay (int): The overall delay of the circuit.
        """
        # Get the levels of all nodes
        levels = self.get_node_levels()

        # Get the levels of output nodes
        output_node_levels = []
        for node_name in self.output_nodes:
            if node_name in levels:
                output_node_levels.append(levels[node_name])
            else:
                raise ValueError(f"Output node {node_name} not found in levels.")

        if not output_node_levels:
            return 0

        # The overall delay is the maximum level among output nodes
        overall_delay = max(output_node_levels)

        return overall_delay
    
    def compute_num_nodes(self):
        return len(self.graph.nodes)
    
    def generate_verilog(self, filename):
        """Generates Verilog code for the Kogge-Stone Adder based on the current circuit structure,
        attaching the corresponding input and output port names to each node as properties."""
        module_name = filename.split('/')[-1].split('.')[0]
        # Basic module definitions
        basic_modules = """
module BigCircle(output G, P, input Gi, Pi, GiPrev, PiPrev);
  wire e;
  and (e, Pi, GiPrev);
  or (G, e, Gi);
  and (P, Pi, PiPrev);
endmodule

module SmallCircle(output Ci, input Gi);
  buf (Ci, Gi);
endmodule

module Square(output G, P, input Ai, Bi);
  and (G, Ai, Bi);
  xor (P, Ai, Bi);
endmodule

module Triangle(output Si, input Pi, CiPrev);
  xor (Si, Pi, CiPrev);
endmodule
"""


        num_bits = len([node for node, data in self.graph.nodes(data=True) if data['type'] == 'input'])
        verilog_code = []

        # Module header
        verilog_code.append(f"module {module_name}(output [{num_bits-1}:0] sum, output cout, input [{num_bits-1}:0] a, b);")
        verilog_code.append("")

        # Initial declarations
        verilog_code.append("  wire cin = 1'b0;")
        verilog_code.append(f"  wire [{num_bits-1}:0] c;")
        verilog_code.append(f"  wire [{num_bits-1}:0] g, p;")
        
        # Initialize `g` and `p` for each input node (Square instantiation)
        for i in range(num_bits):
            node_name = f"Node {i}"
            self.graph.nodes[node_name]['output_ports'] = {'g': f"g[{i}]", 'p': f"p[{i}]"}
        verilog_code.append(f"  Square sq[{num_bits-1}:0](g, p, a, b);")
        verilog_code.append("")

        # Generate Verilog code for each level of the circuit
        levels = self.get_node_levels()
        level_nodes = {}  # Group nodes by levels
        for node, level in levels.items():
            if level not in level_nodes:
                level_nodes[level] = []
            level_nodes[level].append(node)

        for level, nodes in sorted(level_nodes.items()):
            # Skip the initial input level
            if level == 1:
                continue

            # Define wires for generate and propagate signals for this level
            start_index = min(int(node.split()[-1]) for node in nodes)
            end_index = max(int(node.split()[-1]) for node in nodes)
            verilog_code.append(f"  wire [{end_index}:{start_index}] g{level}, p{level};")

            # Process each node in the level as a `BigCircle`
            for node in nodes:
                data = self.graph.nodes[node]
                node_index = data['index']
                preds = list(self.graph.predecessors(node))
                
                # Derive input port names based on predecessors' output ports from the previous level
                left_pred, right_pred = preds
                self.graph.nodes[node]['input_ports'] = {
                    'g_in_left': self.graph.nodes[left_pred]['output_ports']['g'],
                    'p_in_left': self.graph.nodes[left_pred]['output_ports']['p'],
                    'g_in_right': self.graph.nodes[right_pred]['output_ports']['g'],
                    'p_in_right': self.graph.nodes[right_pred]['output_ports']['p']
                }
                
                # Define the output ports for this `BigCircle` node at the current level
                self.graph.nodes[node]['output_ports'] = {
                    'g': f"g{level}[{node_index}]",
                    'p': f"p{level}[{node_index}]"
                }
                
                # Instantiate the BigCircle, using `g{level-1}` and `p{level-1}` for inputs
                verilog_code.append(
                    f"  BigCircle bc{level}_{node_index}(g{level}[{node_index}], p{level}[{node_index}], "
                    f"{self.graph.nodes[right_pred]['output_ports']['g']}, {self.graph.nodes[right_pred]['output_ports']['p']}, "
                    f"{self.graph.nodes[left_pred]['output_ports']['g']}, {self.graph.nodes[left_pred]['output_ports']['p']});"
                )

            verilog_code.append("")

        # Map `c[i]` to output nodes with range `[0:i]`
        for i in range(num_bits):
            # Find the node that computes the range `[0:i]`
            target_node = None
            for node, data in self.graph.nodes(data=True):
                if data.get("range") == (0, i):
                    target_node = node
                    break
            
            if target_node:
                g_output = self.graph.nodes[target_node]['output_ports']['g']
                verilog_code.append(f"  SmallCircle sc{i}(c[{i}], {g_output});")
                self.graph.nodes[target_node]['output_ports']['c_out'] = f"c[{i}]"

        # Instantiate Triangles for final sum generation
        for i in range(num_bits):
            if i == 0:
                verilog_code.append(f"  Triangle tr0(sum[0], p[0], cin);")
            else:
                verilog_code.append(f"  Triangle tr{i}(sum[{i}], p[{i}], c[{i-1}]);")
            # Attach `sum` port to the output of each triangle
            node_name = f"Node {i}"
            self.graph.nodes[node_name]['output_ports']['sum'] = f"sum[{i}]"

        verilog_code.append("")

        # Generate carry-out signal
        verilog_code.append(f"  buf (cout, c[{num_bits-1}]);")
        verilog_code.append("")
        
        # Attach carry-out port to the last node
        last_node_name = f"Node {num_bits - 1}"
        self.graph.nodes[last_node_name]['output_ports']['cout'] = 'cout'
        
        # End the module
        verilog_code.append("endmodule")

        # Join all lines and return the final code
        ksamodule = basic_modules+"\n\n"+"\n".join(verilog_code)
        # Write to file
        with open(filename, "w") as file:
            file.write(ksamodule)
        return ksamodule
    

    def check_circuit_integrity(self):
        """
        Checks the integrity of the prefix circuit:
        - Verifies if each node connects to two nodes with neighbor bit ranges.
        - Checks for missing output signals with computation ranges [0:i].

        Returns:
            bool: True if the circuit is correct; False if there are any issues.
        """
        # Check each prefix node for valid connections
        for node, data in self.graph.nodes(data=True):
            if data["type"] == "prefix":
                bit_range = data["range"]
                predecessors = list(self.graph.predecessors(node))

                # Ensure it connects to exactly two nodes
                if len(predecessors) != 2:
                    print("Not two predecessors!!!")
                    return False  # Incorrect number of connections

                # Check if connected nodes have adjacent bit ranges
                pred_ranges = [self.graph.nodes[pred]["range"] for pred in predecessors]
                pred_ranges.sort()  # Sort ranges to ensure left and right order

                # Verify adjacency of ranges
                if pred_ranges[0][1] + 1 != pred_ranges[1][0] or \
                        (pred_ranges[0][0], pred_ranges[1][1]) != (bit_range[0], bit_range[1]):
                    print(f"Not adjancent range ({pred_ranges[0][0]},{pred_ranges[0][1]}), ({pred_ranges[1][0]},{pred_ranges[1][1]})!!!")
                    return False  # Invalid connection pattern

        # Check for missing output signals with range [0:i] up to the highest output range
        max_range = max(data["range"][1] for node, data in self.graph.nodes(data=True) if data["type"] == "input")
        existing_ranges = {data["range"] for node, data in self.graph.nodes(data=True) if data["type"] == "prefix" and data["range"][0] == 0}
        
        for i in range(1, max_range + 1):
            if (0, i) not in existing_ranges:
                print(f"Missing output with range [0:{i}]")
                return False  # Missing output with range [0:i]

        return True
    
    def get_missing_ranges(self):
        """
        Identifies and returns the missing computation ranges [0:1] up to [0:n],
        where n is the highest bit index in the circuit. Excludes [0:0] as it is an input node.

        Returns:
            list: A list of tuples representing the missing ranges [0:i].
        """
        # Determine the maximum bit index from input nodes
        max_bit_index = max(data["range"][1] for node, data in self.graph.nodes(data=True) if data["type"] == "input")
        
        # Collect existing output ranges [0:i] from prefix nodes
        existing_ranges = {data["range"] for node, data in self.graph.nodes(data=True)
                           if data["type"] == "prefix" and data["range"][0] == 0}

        # Check for missing ranges from [0:1] up to [0:max_bit_index]
        missing_ranges = [(0, i) for i in range(1, max_bit_index + 1) if (0, i) not in existing_ranges]
        
        return missing_ranges
    
    def get_repeated_info(self, range):
        ranges = [data["range"] for node, data in self.graph.nodes(data=True)]
        return True if range in ranges else False
    
    def generate_random_prefix_circuit(self, num_bits, num_prefix_nodes):
        """
        Generates a random, potentially incomplete prefix circuit.

        Parameters:
            num_bits (int): The number of bits for which to generate input nodes.
            num_prefix_nodes (int): The number of prefix nodes to add to the circuit.
        """
        # Clear the current graph
        self.graph.clear()
        self.output_nodes = []

        # Add input nodes
        for i in range(num_bits):
            node_name = f"Node {i}"
            self.graph.add_node(node_name, index=i, range=(i, i), type='input')

        # Initialize with the individual input node ranges
        ranges = [(i, i) for i in range(num_bits)]  # Start with input node ranges
        current_node_index = num_bits  # Start indexing prefix nodes after input nodes

        # Generate the specified number of prefix nodes
        for _ in range(num_prefix_nodes):
            # Randomly pick two adjacent ranges to combine
            if len(ranges) < 2:
                break  # Stop if we don't have enough ranges to combine

            left_range = random.choice(ranges)
            # Ensure right_range is adjacent to left_range
            right_range_candidates = [r for r in ranges if r[0] == left_range[1] + 1]
            if not right_range_candidates:
                continue  # Skip if no adjacent range is found
            
            right_range = random.choice(right_range_candidates)

            # Define the new combined range and add it to the circuit
            combined_range = (left_range[0], right_range[1])
            node_name = f"Node {current_node_index}"
            self.graph.add_node(node_name, index=current_node_index, range=combined_range, type='prefix')
            self.graph.add_edge(f"Node {self._get_node_index(left_range)}", node_name)
            self.graph.add_edge(f"Node {self._get_node_index(right_range)}", node_name)

            # Update ranges list by removing the combined ranges and adding the new range
            ranges.remove(left_range)
            ranges.remove(right_range)
            ranges.append(combined_range)
            current_node_index += 1

            # Randomly decide if this node should be an output node for `[0:i]` range
            if combined_range[0] == 0 and random.choice([True, False]):
                self.output_nodes.append(node_name)

    def _get_node_index(self, bit_range):
        """
        Helper function to find the node index with a given bit range.
        """
        for node, data in self.graph.nodes(data=True):
            if data["range"] == bit_range:
                return data["index"]
        return None
    
    def add_random_prefix_node(self):
        """
        Randomly generates and adds a prefix node to the current prefix circuit, 
        potentially making the circuit more complete.
        """
        # Collect all ranges currently in the circuit
        ranges = [data["range"] for node, data in self.graph.nodes(data=True)]

        # Check if we have enough ranges to combine (need at least two adjacent ranges)
        if len(ranges) < 2:
            print("Not enough ranges to combine.")
            return None  # Exit if we don't have enough ranges

        # Randomly select two adjacent ranges
        left_range = random.choice(ranges)
        right_range_candidates = [r for r in ranges if r[0] == left_range[1] + 1]

        if not right_range_candidates:
            print("No adjacent range found for the selected range.")
            return None  # Exit if no adjacent range is found

        right_range = random.choice(right_range_candidates)

        # Define the new combined range
        combined_range = (left_range[0], right_range[1])

        # Assign a new index for the prefix node
        current_node_index = max(data["index"] for node, data in self.graph.nodes(data=True)) + 1
        node_name = f"Node {current_node_index}"

        # Add the new prefix node to the graph
        self.graph.add_node(node_name, index=current_node_index, range=combined_range, type='prefix')
        self.graph.add_edge(f"Node {self._get_node_index(left_range)}", node_name)
        self.graph.add_edge(f"Node {self._get_node_index(right_range)}", node_name)

        # Randomly decide if this node should be an output node for the `[0:i]` range
        if combined_range[0] == 0 and random.choice([True, False]):
            self.output_nodes.append(node_name)

        print(f"Added prefix node {node_name} with range {combined_range}.")
        return node_name
    
    @staticmethod
    def non_dominated_sort(circuits):
        """
        Performs non-dominated sorting on a list of PrefixCircuit instances based on area and delay,
        returning a single list with circuits ordered by Pareto dominance.

        Parameters:
            circuits (list of PrefixCircuit): List of circuits to sort.

        Returns:
            list: A single sorted list of PrefixCircuit instances, ordered by Pareto frontiers.
        """
        # Compute area and delay for each circuit and store as tuples (area, delay, circuit)
        circuit_metrics = [(circuit.compute_num_nodes(), circuit.compute_overall_delay(), circuit) for circuit in circuits]

        # Initialize data structures for non-dominated sorting
        frontiers = []  # List of Pareto frontiers
        dominated_solutions = {i: [] for i in range(len(circuit_metrics))}  # Tracks circuits dominated by each circuit
        domination_counts = [0] * len(circuit_metrics)  # Number of circuits dominating each circuit

        # Calculate domination relationships
        for i, (area_i, delay_i, circuit_i) in enumerate(circuit_metrics):
            for j, (area_j, delay_j, circuit_j) in enumerate(circuit_metrics):
                if i == j:
                    continue
                # Check if circuit i dominates circuit j
                if (area_i <= area_j and delay_i <= delay_j) and (area_i < area_j or delay_i < delay_j):
                    dominated_solutions[i].append(j)
                # Check if circuit j dominates circuit i
                elif (area_j <= area_i and delay_j <= delay_i) and (area_j < area_i or delay_j < delay_i):
                    domination_counts[i] += 1

        # Identify first Pareto frontier (non-dominated solutions)
        first_frontier = [i for i, count in enumerate(domination_counts) if count == 0]
        current_frontier = first_frontier

        # Construct each frontier iteratively and add to a single list
        sorted_circuits = []

        while current_frontier:
            # Add current frontier circuits to the sorted list
            sorted_circuits.extend([circuit_metrics[i][2] for i in current_frontier])
            next_frontier = []

            for i in current_frontier:
                for j in dominated_solutions[i]:
                    domination_counts[j] -= 1  # Reduce domination count for dominated circuits
                    if domination_counts[j] == 0:
                        next_frontier.append(j)  # Add to next frontier if no other circuit dominates it

            current_frontier = next_frontier

        return sorted_circuits

    @staticmethod
    def parse_circuits_from_file(filename, prune_node_flag=True):
        """
        Parses the text file to create multiple PrefixCircuit instances.

        Parameters:
            filename (str): Path to the file containing the prefix circuit data.

        Returns:
            list of PrefixCircuit: List of created PrefixCircuit instances.
        """
        circuits = []
        with open(filename, 'r') as file:
            circuit_text = ""
            read_state = 0
            for line in file:
                if "area:" in line:
                    read_state = 0
                    pc = PrefixCircuit()
                    pc.construct_circuit_from_info_string(circuit_text)
                    if prune_node_flag:
                        pc.remove_useless_nodes()
                    circuits.append(pc)
                    circuit_text = ""
                if read_state:
                    circuit_text += line
                if "prefix circuit:" in line:
                    read_state = 1
        return circuits
    
    @staticmethod
    def plot_pareto_front(circuits, filename):
        """
        Plots the Pareto front of circuits based on area and delay.

        Parameters:
            circuits (list of PrefixCircuit): List of PrefixCircuit instances.
        """
        sorted_circuits = PrefixCircuit.non_dominated_sort(circuits)
        areas = [circuit.compute_num_nodes() for circuit in sorted_circuits]
        delays = [circuit.compute_overall_delay() for circuit in sorted_circuits]

        plt.figure(figsize=(10, 6))
        plt.scatter(areas, delays, color="gray", label="All Circuits")
        # plt.scatter(areas[:len(circuits)], delays[:len(circuits)], color="red", label="Pareto-Optimal Circuits")
        plt.xlabel("Area")
        plt.ylabel("Delay")
        plt.legend()
        plt.grid(True)
        plt.title("Pareto Front for Prefix Circuits")
        plt.savefig(f"{filename}.png")

    @staticmethod
    def sort_circuits_by_area(circuits):
        """
        Sorts a list of PrefixCircuit instances by area in descending order.

        Parameters:
            circuits (list of PrefixCircuit): List of circuits to be sorted.

        Returns:
            list of PrefixCircuit: A new list of circuits sorted by area in descending order.
        """
        # Sort circuits by area in descending order
        sorted_circuits = sorted(circuits, key=lambda circuit: circuit.compute_num_nodes(), reverse=True)
        return sorted_circuits
    
    def remove_useless_nodes(self):
        """
        Removes prefix nodes that are not connected (either directly or indirectly) to any output node.
        """
        # Find all prefix nodes in the circuit
        prefix_nodes = [node for node, data in self.graph.nodes(data=True) if data["type"] == "prefix"]

        # Check each prefix node to see if it has a path to any output node
        removed_nodes = []
        for node in prefix_nodes:
            # If there is no path from this prefix node to any output node, it's "useless"
            if not any(nx.has_path(self.graph, node, output_node) for output_node in self.output_nodes):
                removed_nodes.append(node)
        
        for node in removed_nodes:
            self.graph.remove_node(node)
        
        self._reindex_nodes()

    def _reindex_nodes(self):
        """
        Reindexes the nodes to ensure continuous indexes after nodes have been removed.
        """
        # Generate a mapping from the current node names to new consecutive indices
        sorted_nodes = sorted(self.graph.nodes(), key=lambda node: int(node.split(" ")[1]))

        node_mapping = {old_node: f"Node {i}" for i, old_node in enumerate(sorted_nodes)}
        node_id_mapping = {old_node: i for i, old_node in enumerate(self.graph.nodes())}
        
        for old_node in node_id_mapping:
            self.graph.nodes[old_node]['index'] = node_id_mapping[old_node]
        # Apply the relabeling
        # nx.relabel_nodes(self.graph, node_mapping,copy=False)
        # sorted(self.graph)
        # Update output_nodes with new names
        # self.output_nodes = [node_mapping[node] for node in self.output_nodes]
    
    def get_known_init(self, file_path, num_bits = 0, cell_map = None):

        def update_level_map(cell_map, index_map, level_map):
            level_map.fill(0)
            level_map[0, 0] = 1

            for x in range(0,num_bits):
                index_map[x,x] = x

            for x in range(1,num_bits):
                level_map[x, x] = 1
                last_y = x
                for y in range(x-1, -1, -1):
                    if cell_map[x, y] == 1:
                        left_node_index = int(index_map[last_y-1, y])
                        right_node_index = int(index_map[x,last_y])


                        self.add_prefix_node(left_node_index,right_node_index,len(self.graph.nodes))

                        index_map[x,y] = len(self.graph.nodes) - 1
                        level_map[x, y] = max(level_map[x, last_y], level_map[last_y-1, y])+ 1
                        last_y = y
            return level_map, index_map
        
        for i in range(num_bits):
            self.add_input_node(i,(i,i))

        if cell_map is None:
            fopen = open(file_path, "r")
            cell_map = np.zeros((num_bits, num_bits))
            i = 0
            for line in fopen.readlines():
                item_list = line.strip().split()
                # print("item_list", item_list)
                for j, x in enumerate(item_list):
                    cell_map[i, j] = int(x)
                i += 1
        
        level_map = np.zeros((num_bits, num_bits))
        index_map = np.zeros((num_bits, num_bits))
        level_map,index_map = update_level_map(cell_map, index_map, level_map)

        print("READ level = {}, size = {}".format(level_map.max(), cell_map.sum()))

        print(self.print_circuit_info())
        print(f"area:{self.compute_num_nodes()}")
        print(f"delay:{self.compute_overall_delay()}")


        


        
if __name__ == '__main__':

    def generate_sk_matrix(INPUT_BIT,matrix_path):
        cell_map = np.zeros((INPUT_BIT, INPUT_BIT))
        level_map = np.zeros((INPUT_BIT, INPUT_BIT))
        for i in range(INPUT_BIT):
            cell_map[i, i] = 1
            level_map[i, i] = 1
            t = i
            now = i
            x = 1
            level = 1
            while t > 0:
                if t % 2 ==1:
                    last_now = now
                    now -= x
                    cell_map[i, now] = 1
                    level_map[i, now] = max(level, level_map[last_now-1, now]) +1
                    level += 1
                t = t // 2
                x *= 2
        np.savetxt(matrix_path, cell_map, fmt='%d')

    # generate_sk_matrix(8,"test_sk_matrix.txt")

    circuit = PrefixCircuit()
    circuit.get_known_init("adder_16b_5l_49s_0.txt",16)
    
    filename = "GPTPrefix16_L8_TrajectoryTrunc_it13.txt"
    circuits = PrefixCircuit.parse_circuits_from_file(filename)
    for circuit in circuits:
        print("Prefix circuit:")
        print(circuit.print_circuit_info())
        print("Area:")
        print(circuit.compute_num_nodes())

        
    PrefixCircuit.plot_pareto_front(circuits, 'GPTPrefix16')


    circuit = PrefixCircuit()
    prefix_str = '''
    0: connectedNodes=(None, None), range=[0:0], left_bound=0, right_bound=0.
    1: connectedNodes=(None, None), range=[1:1], left_bound=1, right_bound=1.
    2: connectedNodes=(None, None), range=[2:2], left_bound=2, right_bound=2.
    3: connectedNodes=(None, None), range=[3:3], left_bound=3, right_bound=3.
    4: connectedNodes=(None, None), range=[4:4], left_bound=4, right_bound=4.
    5: connectedNodes=(None, None), range=[5:5], left_bound=5, right_bound=5.
    6: connectedNodes=(None, None), range=[6:6], left_bound=6, right_bound=6.
    7: connectedNodes=(None, None), range=[7:7], left_bound=7, right_bound=7.
    8: connectedNodes=(0, 1), range=[0:1], left_bound=0, right_bound=1.
    9: connectedNodes=(8, 2), range=[0:2], left_bound=0, right_bound=2.
    10: connectedNodes=(9, 3), range=[0:3], left_bound=0, right_bound=3.
    11: connectedNodes=(4, 5), range=[4:5], left_bound=4, right_bound=5.
    12: connectedNodes=(10, 11), range=[0:5], left_bound=0, right_bound=5.
    13: connectedNodes=(6, 7), range=[6:7], left_bound=6, right_bound=7.
    14: connectedNodes=(12, 13), range=[0:7], left_bound=0, right_bound=7.
    15: connectedNodes=(3, 4), range=[3:4], left_bound=3, right_bound=4.
    16: connectedNodes=(9, 15), range=[0:4], left_bound=0, right_bound=4.
    17: connectedNodes=(12, 6), range=[0:6], left_bound=0, right_bound=6.
    '''
    circuit.construct_circuit_from_info_string(prefix_str)
    print(f"area:{circuit.compute_num_nodes()}, delay:{circuit.compute_overall_delay()}")
    circuit.generate_verilog('./GPTPrefixCircuit/prefixcircuit8.v')

    
    # circuit.build_ripple_carry_circuit(8)
    # info = circuit.print_circuit_info()
    # print(info)

    # circuit.visualize()

    kscircuit = PrefixCircuit()
    kscircuit.build_kogge_stone_circuit(8)
    print(f"area:{kscircuit.compute_num_nodes()}, delay:{kscircuit.compute_overall_delay()}")

    rcacircuit = PrefixCircuit()
    rcacircuit.build_ripple_carry_circuit(8)
    print(f"area:{rcacircuit.compute_num_nodes()}, delay:{rcacircuit.compute_overall_delay()}")
    
    circuits = [circuit,kscircuit,rcacircuit]
    results = PrefixCircuit.non_dominated_sort(circuits)
    print(results)
    # kscircuit.visualize()
    # print(kscircuit.generate_verilog("KSA8.v"))
    
    # # Add input nodes
    # for i in range(8):
    #     circuit.add_input_node(index=i, bit_range=(i, i))

    # # Step 1: Combine Node 0 and Node 1 into Node 8 (Range: [0:1])
    # circuit.add_prefix_node(left_node_index=0, right_node_index=1, index=8)

    # # Step 2: Combine Node 2 and Node 3 into Node 9 (Range: [2:3])
    # circuit.add_prefix_node(left_node_index=2, right_node_index=3, index=9)

    # # Step 3: Combine Node 8 and Node 9 into Node 10 (Range: [0:3])
    # circuit.add_prefix_node(left_node_index=8, right_node_index=9, index=10)

    # # Step 4: Combine Node 4 and Node 5 into Node 11 (Range: [4:5])
    # circuit.add_prefix_node(left_node_index=4, right_node_index=5, index=11)

    # # Step 5: Combine Node 6 and Node 7 into Node 12 (Range: [6:7])
    # circuit.add_prefix_node(left_node_index=6, right_node_index=7, index=12)

    # # Step 6: Combine Node 11 and Node 12 into Node 13 (Range: [4:7])
    # circuit.add_prefix_node(left_node_index=11, right_node_index=12, index=13)

    # # Step 7: Combine Node 10 and Node 13 into Node 14 (Range: [0:7])
    # circuit.add_prefix_node(left_node_index=10, right_node_index=13, index=14)

    # # Step 8: Combine Node [0:2]
    # circuit.add_prefix_node(left_node_index=8,right_node_index=2, index=15)

    # # Step 9: Range: [0:4]
    # circuit.add_prefix_node(left_node_index=10,right_node_index=4,index=16)

    # # Step 10: Range: [0:5]
    # circuit.add_prefix_node(left_node_index=10,right_node_index=11,index=17)

    # # Step 11: Range: [0:6]
    # circuit.add_prefix_node(left_node_index=17, right_node_index=6, index=18)
    # # Visualize the circuit
    # circuit.visualize()
