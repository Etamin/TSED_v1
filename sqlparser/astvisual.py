import json
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, node):
        self.children.append(node)

def create_tree(json_obj, parent=None):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if value is not None:
                node = Node(key)
                parent.add_child(node)
                create_tree(value, node)
    elif isinstance(json_obj, list):
        for item in json_obj:
            create_tree(item, parent)
    else:
        node = Node(json_obj)
        parent.add_child(node)

def draw_graph(node, graph=None):
    if graph is None:
        graph = nx.DiGraph()
    for child in node.children:
        graph.add_edge(node.name, child.name)
        draw_graph(child, graph)
    return graph

json_str = """
{
  "with": null,
  "type": "select",
  "options": null,
  "distinct": "DISTINCT",
  "columns": [ { "expr": [{}], "as": null } ],
  "from": [
    { "db": null, "table": "Beneficiary", "as": null },
    {
      "db": null,
      "table": "Transactions",
      "as": null,
      "join": "INNER JOIN",
      "on": [{}]
    }
  ],
  "where": {
    "type": "binary_expr",
    "operator": "=",
    "left": { "type": "column_ref", "table": null, "column": "client_id" },
    "right": { "type": "number", "value": 996720 }
  },
  "groupby": null,
  "having": null,
  "orderby": null,
  "limit": null
}
"""
json_obj = json.loads(json_str)
root = Node('root')
create_tree(json_obj, root)

graph = draw_graph(root)
pos = graphviz_layout(graph, prog='neato')
nx.draw(graph, pos, with_labels=True)
plt.show()
