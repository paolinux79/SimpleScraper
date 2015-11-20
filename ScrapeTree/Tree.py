__author__ = 'paolinux'

from Node import Node
import json

class Tree:

    tree = None

    def __init__(self):
        self.tree = {}


    def add_node(self, node):
        current_length = len(self.tree)
        node_id = current_length
        self.tree[node_id] = node
        return node_id

    def get_node(self, node_id):
        return self.tree[node_id]


    def out(self):
        out_dict = {}
        for k,v in self.tree.items():
            out_dict[k] = v.__dict__
        return out_dict



def main():
    new_tree = Tree()

    new_node = Node(url='ma suka', score=33, matchings={}, tree=new_tree)
    node_id = new_tree.add_node(new_node)
    new_node.set_node_id(node_id)
    new_node.add_parent(parent_id=0)



if __name__ == '__main__':
    main()
