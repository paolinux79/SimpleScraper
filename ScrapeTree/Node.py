__author__ = 'paolinux'
from urlparse import urlparse
import json



class Node:

    node = None

    def __init__(self,url,score,matchings,tree):
        self.node = {}
        self.node['children'] = []
        self.node['parent'] = -1
        self.node['own_score'] = score
        self.node['total_score'] = 0
        self.node['url'] = url
        self.node['domain'] = get_domain(url)
        self.node['matchings'] = matchings
        self.node['tree'] = tree
        self.node['own_id'] = 0
        self.node['level'] = 0

    def add_parent(self, parent_id):
        self.node['parent'] = parent_id
        self.node['tree'].get_node(parent_id).__add_score__(self.node['own_score'])
        self.node['tree'].get_node(parent_id).__add_child__(self.node['own_id'])
        self.node['level'] = self.node['tree'].get_node(parent_id).get_level() + 1

    def set_node_id(self, own_id):
        self.node['own_id'] = own_id

    def get_node_id(self):
        return self.node['own_id']

    def get_parent_id(self):
        return self.node['parent']

    def get_level(self):
        return self.node['level']

    def __add_child__(self, child_id):
        self.node['children'].append(child_id)

    def __add_score__(self,score_to_add):
        self.node['total_score'] += score_to_add




def get_domain(link):
    parsed_uri = urlparse(link)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain



