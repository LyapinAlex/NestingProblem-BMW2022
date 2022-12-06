
class GraphNode:
    def __init__(self) -> None:
        self.half_edge = None
        self.connected_nodes: list[GraphNode] = []
        self.is_hole: bool = False

    def get_all_neighbours(self, nodes):
        nodes.append(self)
        for connected_node in self.connected_nodes:
            if (connected_node not in nodes):
                connected_node.get_all_neighbours(nodes)

    def __eq__(self, other) -> bool:
        if (self.half_edge is None and other.half_edge is None):
            return False
        if (self.half_edge is None or other.half_edge is None):
            return False
        return self.half_edge.origin == other.half_edge.origin and self.half_edge.end == other.half_edge.end


class Graph:
    def __init__(self) -> None:
        self.nodes: list[GraphNode] = []

    def create_node(self):
        node = GraphNode()
        self.nodes.append(node)
        return node

    def connect_nodes(self, first_node, second_node):
        first_node.connected_nodes.append(second_node)
        second_node.connected_nodes.append(first_node)

    def get_all_neighbours(self, node: GraphNode):
        nodes = []
        for connected_node in node.connected_nodes:
            connected_node.get_all_neighbours(nodes)
        return nodes
