import re
from ete3 import Tree


class TreeCreator:
    def __init__(self, json_dict):
        self.json_dict = json_dict

    def init_map_of_codes(self):
        map = {}
        with open('static/Model/miRbase_codes_names.txt') as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        for code in content:
            s = code.split('	')
            map[s[0]] = s[1]
        return map

    def create_newick(self, newick):
        with open(newick, 'r') as myfile:
            map_of_codes = self.init_map_of_codes()
            tree_str = myfile.read().replace('\n', '')
            tree_names = re.split('[\s+\n+\"\'\:\)\(\,\:\'\']', tree_str)
            tree_names = list(filter(lambda x: x != "" and x != ';', tree_names))
            for name in tree_names:
                tree_str = tree_str.replace(name, map_of_codes[name])

            return tree_str

    def create_tree(self, newick):
        with open(newick, 'r') as myfile:
            map_of_codes = self.init_map_of_codes()
            tree_str = myfile.read().replace('\n', '')
            tree_names = re.split('[\s+\n+\"\'\:\)\(\,\:\'\']', tree_str)
            tree_names = list(filter(lambda x: x != "" and x != ';', tree_names))
            for name in tree_names:
                tree_str = tree_str.replace(name, map_of_codes[name])

            result = Tree(tree_str)
            return result