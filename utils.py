def setup_transmission_chain(connections, NODE_CLS, task, sim_id=0):
    """
    Initializes the chain. 

    Args:
        connection (list(list)): index of the inner list is the generation, each element in the inner list is a node in that generation

    Example:
        connections = [
    [[1], [1], [2]], # 0th generation; their outgoing connections
    [[0], [0, 1, 2], [2]] # 1st generation; their outgoing connections
    ]

    represents the input for 

    # 0    0 - 0
    #   \   /
    # 1 - 1 - 1
    #       \
    # 2 - 2 - 2
    """
    last_nodes = set(node for out_node_list in connections[-1] for node in out_node_list)
    connections = connections.copy()
    connections.append([[] for _ in last_nodes])
    
    
    all_nodes = []
    incoming_connections_next_generation = []
    
    for gen_id, generation in enumerate(connections):
        generation_nodes = []
        
        if gen_id < len(connections) - 1:
            incoming_connections_next_generation.append([[] for _ in connections[gen_id + 1]])
    
        for node_id, outgoing in enumerate(generation):
            node = NODE_CLS((gen_id, node_id), task=task, sim_id=sim_id)
            generation_nodes.append(node)
    
            if gen_id < len(connections) - 1:
                for out_id in outgoing:
                    incoming_connections_next_generation[-1][out_id].append(node)
    
        all_nodes.append(generation_nodes)
    
    for gen_id, generation in enumerate(all_nodes):
        for node in generation:
            if gen_id > 0:
                node.receive_input_from = incoming_connections_next_generation[gen_id-1][node.id[1]]
    
            if gen_id < len(all_nodes) - 1:
                node.send_output_to = [all_nodes[gen_id + 1][out_id] for out_id in connections[gen_id][node.id[1]]]

    return all_nodes