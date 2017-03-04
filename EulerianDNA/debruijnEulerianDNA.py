import random


def find_eulerian_tour(graph, d, tour):
    edge_val = list(graph.keys())[0]
    # creating a new tour
    tour.append([])
    tour_number = len(tour) - 1
    while graph.get(edge_val):
        node_val = graph[edge_val][0]
        graph[edge_val].pop(0)
        tour[tour_number].append(node_val)
        # checking the node is empty
        if not graph.get(edge_val):
            graph.pop(edge_val)
        # update the edge val
        edge_val = node_val[d - len(edge_val):]
    if graph:
        # there are still some untraversed nodes, recurrsive call
        find_eulerian_tour(graph, d, tour)
    return tour


def generate_random_read(n):
    """
    :param n:
    :return:
    """
    possible_acetites = ["A", "C", "G", "T"]
    generated_read = ""
    for i in range(n):
        generated_read += random.choice(possible_acetites)

    return generated_read


def split_reads(read, d):
    """

    :param read:
    :param d:
    :return:
    """
    prev_c = 0
    c = 0
    reads = []
    # adding one to make sure the last read also gets selected
    for c in range(d, len(read), d):
        # ToDo: Make generic logic for pairs
        first = read[prev_c: c]
        second = read[prev_c + 1: c + 1]
        third = read[prev_c + 2: c + 2]
        reads.append(first)
        reads.append(second)
        reads.append(third)
        prev_c = c
    return reads


def generate_graph_from_reads(splitted_reads):
    debruijn_graph = {}
    for split in splitted_reads:
        # node value would be one less than that edge
        node_val = split[:len(split) - 1]
        # if the node was already there, then append the edge to the same node, else create a new node
        if not debruijn_graph.get(node_val):
            # creating new node
            debruijn_graph[node_val] = [split]
        else:
            # appending edge
            debruijn_graph[node_val].append(split)
    # returning the graph
    return debruijn_graph


def pretty_print_tour(eu_tours):
    for tour in eu_tours:
        print(' -> '.join(tour))


def merge_eu_path(eu_tours):
    final_eu = []
    if len(eu_tours) > 1:
        for tour in eu_tours:
            # first part matches the last part of any tour
            part_to_match = tour[0][:2]
            parts_could_merge = [t for t in eu_tours if t[len(t) - 1][1:] == part_to_match]
            if parts_could_merge:
                final_eu.append(parts_could_merge[0] + tour)
                eu_tours.pop(eu_tours.index(parts_could_merge[0]))
            else:
                final_eu.append(tour)
    else:
        return eu_tours

    return final_eu


if __name__ == "__main__":
    # the read splitting currently works for split size, logic can be improved to handle generalized split size
    read_split_size = 3
    # length of n character string, randomly generated, multiple of split size preferably
    DNA_read = generate_random_read(read_split_size * 5)

    # with random string, the result is not exact match, as there are multiple collusion paths
    # DNA_read = 'ACGTACGT'
    # DNA_read = 'TAATGCCATGGGATGTAT'
    # DNA_read = 'CCAGTATTGCACGTA'
    print(DNA_read)
    # this will break the string into format
    splitted_reads = split_reads(DNA_read, read_split_size)
    # print splitted_reads.pop(5)
    print(splitted_reads)
    graph = generate_graph_from_reads(splitted_reads)
    print(graph)
    eu_tour = find_eulerian_tour(graph, read_split_size, [])
    print('Without merging path:')
    pretty_print_tour(eu_tour)
    eu_tour = merge_eu_path(eu_tour)
    print('After merging path:')
    pretty_print_tour(eu_tour)
    # should always find a path as the read was generated from a connected string...
    # print(find_eulerian_tour(graph))
