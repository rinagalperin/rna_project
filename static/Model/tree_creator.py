class TreeCreator:
    def __init__(self, json_dict):
        # paths configurations
        self.newick_path = 'static/Model/miRbase_newick.txt'
        self.organisms_code_names_path = 'static/Model/miRbase_codes_names.txt'

        # instantiations
        self.short_name_to_full_name_map = {}
        self.full_name_to_short_name_map = {}
        self.json_dict = json_dict
        self.newick = self.init_newick()

        # initializations
        self.init_name_maps()

    def init_name_maps(self):
        map_1 = {}
        with open(self.organisms_code_names_path) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        for code in content:
            s = code.split('	')
            map_1[s[0]] = s[1]
        self.short_name_to_full_name_map = map_1

        map_2 = {}
        # tree_str = self.newick
        # tree_names = re.split('[\s+\n+\"\'\:\)\(\,\:\'\']', tree_str)
        # tree_names = list(filter(lambda x: x != "" and x != ';', tree_names))
        for short_name in self.short_name_to_full_name_map.keys():
            full_name = self.short_name_to_full_name_map[short_name]
            map_2[full_name] = short_name

        self.full_name_to_short_name_map = map_2

    def get_short_organism_name(self, full_name):
        return self.full_name_to_short_name_map[full_name]

    def get_full_organism_name(self, short_name):
        return self.short_name_to_full_name_map[short_name]

    def init_newick(self):
        with open(self.newick_path, 'r') as myfile:
            tree_str = myfile.read().replace('\n', '')

        return tree_str
