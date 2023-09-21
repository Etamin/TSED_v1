import subprocess
import json
import networkx as nx
from apted import APTED
from apted.helpers import Tree
import sys
import os


class Node:
    def __init__(self, name, path):
        self.id = path
        self.name = name
        self.children = []

    def add_child(self, node):
        self.children.append(node)


def run_js(js_file, sql_query):
    result = subprocess.run(['node', js_file, sql_query], capture_output=True, text=True)
    return result.stdout



def create_tree(json_obj, parent=None, parent_path=""):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if value is not None:
                node_path = parent_path + '/' + key
                node = Node(key, node_path)
                parent.add_child(node)
                create_tree(value, node, node_path)
    elif isinstance(json_obj, list):
        for index, item in enumerate(json_obj):
            node_path = parent_path + '/' + str(index)
            create_tree(item, parent, node_path)
    else:
        node_path = parent_path + '/' + str(json_obj)
        node = Node(json_obj, node_path)
        parent.add_child(node)


def draw_graph(node, graph=None):
    if graph is None:
        graph = nx.DiGraph()
    for child in node.children:
        graph.add_edge(node.id, child.id)
        graph.nodes[node.id]['label'] = node.name
        graph.nodes[child.id]['label'] = child.name
        draw_graph(child, graph)
    return graph


def dfs_tree_to_string(node, tree):
    children = list(tree.successors(node))
    if len(children) == 0:
        return f"{{{node}}}"
    else:
        children_strs = ''.join(dfs_tree_to_string(child, tree) for child in children)
        return f"{{{node}{children_strs}}}"


def to_tree(sql_query):
    js_output = run_js('./sqlparser/run.js', sql_query)
    json_obj = json.loads(js_output)
    root = Node('root', 'root')
    create_tree(json_obj, root, 'root')  
    graph = draw_graph(root)
    return dfs_tree_to_string('root', graph)


def TSED(sql_query1,sql_query2):


    if sql_query1=="" or sql_query2=="":
        return (0.0)
    else:
        try:
            tree_string1 = to_tree(sql_query1.lower())
            tree_string2 = to_tree(sql_query2.lower())
        except:
            return (0.0)
        # print(tree_string1)
        tree1 = Tree.from_text(tree_string1)
        tree2 = Tree.from_text(tree_string2)
        len1=str(tree1).count('}')
        len2=str(tree2).count('}')
        # print(tree1)
        # print(tree2)
        maxlen=max(len1,len2)
        apted = APTED(tree1, tree2)
        res = apted.compute_edit_distance()
        if res>maxlen:
            res=maxlen
        return(float(1-(res/maxlen)))


