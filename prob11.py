from dataclasses import dataclass

@dataclass
class Node:
    id: str
    children: tuple["Node"] = ()
    visits: int = 0
    temp_mark: bool = False
    perm_mark: bool = False

    def __str__(self):
        return f'Node({self.id})'
    def __repr__(self):
        return str(self)


def get_or(dict_obj, k, default):
    if k not in dict_obj:
        dict_obj[k] = default
        return default
    return dict_obj[k]


def build_graph(input_path: str):
    with open(input_path) as f:
        lines = f.readlines()
    
    nodes = {}
    for line in lines:
        cur_id, rest = line.strip().split(': ')
        other_ids = rest.split(' ')

        cur_node = get_or(nodes, cur_id, Node(cur_id))
        children = [get_or(nodes, c_id, Node(c_id)) for c_id in other_ids]
        cur_node.children = tuple(children)
    return nodes


def solve_1_dfs_traverse(nodes: dict[str, Node]):

    def visitor(cur_node: Node, prev_node: Node | None = None):
        cur_node.visits += 1
        for child in cur_node.children:
            visitor(child, cur_node)
    
    start = nodes['you']
    visitor(start)


def solve_2_dfs_traverse(nodes: dict[str, Node]):
    contains_dac = False
    contains_fft = False
    cur_path = set()

    def visitor(cur_node: Node):
        print(','.join(cur_path))
        nonlocal contains_dac, contains_fft
        if cur_node.id in cur_path:
            print(cur_node.id, "CYCLE")
            return

        cur_path.add(cur_node.id)
        # if cur_node.id == 'dac':
        #     contains_dac = True
        # if cur_node.id == 'fft':
        #     contains_fft = True

        # if contains_fft and contains_dac:
        #     cur_node.visits += 1
        cur_node.visits += 1
        for child in cur_node.children:
            visitor(child)
        
        cur_path.remove(cur_node.id)

        # if cur_node.id == 'dac':
        #     contains_dac = False
        # if cur_node.id == 'fft':
        #     contains_fft = False   
    
    start = nodes['you']
    visitor(start)


def topological_sort(nodes: dict[str, Node]):
    sorted_nodes = []
    debug = False
    def dfs_visit(node: Node):
        if debug: 
            print(f"{node.id=}, {node.perm_mark=} {node.temp_mark=}")
        if node.perm_mark:
            return
        if node.temp_mark:
            raise RuntimeError('Cycle')
        
        node.temp_mark = True
        for child in node.children:
            dfs_visit(child)
        
        node.perm_mark = True
        sorted_nodes.append(node)
    

    unmarked = [n for n in nodes.values() if not n.perm_mark]
    while unmarked:
        n = unmarked.pop()
        dfs_visit(n)
        unmarked = [n for n in nodes.values() if not n.perm_mark]
    return list(reversed(sorted_nodes))


def solve_v2_topo_sort(nodes: dict[str, Node]):
    topo = topological_sort(nodes)
    id_to_index = {n.id: i for i, n in enumerate(topo)}
    
    pathsFromSVR = [int(n.id == 'svr') for n in topo]
    pathsFromFFT = [int(n.id == 'fft') for n in topo]
    pathsFromDAC = [int(n.id == 'dac') for n in topo]
    
    for u in topo:
        for v in u.children:
            u_idx = id_to_index[u.id]
            v_idx = id_to_index[v.id]

            pathsFromSVR[v_idx] += pathsFromSVR[u_idx]
            pathsFromFFT[v_idx] += pathsFromFFT[u_idx]
            pathsFromDAC[v_idx] += pathsFromDAC[u_idx]
    
    svr_to_fft = pathsFromSVR[id_to_index['fft']]
    fft_to_dac = pathsFromFFT[id_to_index['dac']]
    dac_to_out = pathsFromDAC[id_to_index['out']]

    svr_to_dac = pathsFromSVR[id_to_index['dac']]
    dac_to_fft = pathsFromDAC[id_to_index['fft']]
    fft_to_out = pathsFromFFT[id_to_index['out']]
    
    fwd = svr_to_fft * fft_to_dac * dac_to_out
    bwd = svr_to_dac * dac_to_fft * fft_to_out
    return fwd + bwd

    # print(topo)
    # print(dp)




if __name__ == '__main__':
    G = build_graph('data/prob-11.txt')
    res = solve_v2_topo_sort(G)
    print(res)
    # sortedG = topological_sort(G)
    # print(sortedG)
    # solve_1_dfs_traverse(G)
    # solve_2_dfs_traverse(G)
    # print(G['out'])

    # rprint(G['aaa'])

