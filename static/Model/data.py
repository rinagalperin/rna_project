import json
from collections import defaultdict
from os.path import commonprefix
import numpy as np
import operator

from static.Model.mature import Mature
from static.Model.mapper import create_map_5p_3p, init_p, get_all_seed, map_seed_to_organisms_extended


class Data:
    def __init__(self, seed_length):
        self.seed_length = seed_length

        # pre-mir-name: cin-mir-4074
        # to ->
        # seed: AACGUU
        self.pre_mir_name_to_seeds_map = {}

        # pre-mir-name: cin-mir-4074
        # to ->
        # mature-name-and-type: {{cin-miR-4074-3p, 3p}}
        self.pre_mir_name_to_mature_5p_or_3p_map = {}

        self.table_data = self.table_from_txt_file("static/Model/hairpin.txt")
        self.seed_list = get_all_seed(self.table_data)
        self.organisms = np.unique(self.table_data[1])

        #self.create_seed_mature_name_map_file()
        self.seed_mature_name_map = self.init_seed_mature_name_map()
        self.mature_name_seed_map = self.init_mature_name_seed_map()

    def table_from_txt_file(self, path_input):
        pname_to_data = create_map_5p_3p("static/Model/mature.txt")
        with open(path_input, "r") as f:
            split_txt = f.read().split('>')

        preMirName = []
        organisms = []
        preMirSeq = []

        fivePMatureMirName = []
        fivePMatureMirSeq = []
        fivePMatureMirSeed = []

        threePMatureMirName = []
        threePMatureMirSeq = []
        threePMatureMirSeed = []

        metazoaFamilies = [
            "Xenoturbella bocki",
            "Branchiostoma belcheri",
            "Branchiostoma floridae",
            "Ciona intestinalis",
            "Ciona savignyi",
            "Oikopleura dioica",
            "Petromyzon marinus",
            "Xenopus laevis",
            "Xenopus tropicalis",
            "Anas platyrhynchos",
            "Columba livia",
            "Gallus gallus",
            "Taeniopygia guttata",
            "Callorhinchus milii",
            "Echinops telfairi",
            "Canis familiaris",
            "Dasypus novemcinctus",
            "Oryctolagus cuniculus",
            "Artibeus jamaicensis",
            "Bubalus bubalis",
            "Equus caballus",
            "Eptesicus fuscus",
            "Pteropus alecto",
            "Monodelphis domestica",
            "Macropus eugenii",
            "Sarcophilus harrisii",
            "Ateles geoffroyi",
            "Lagothrix lagotricha",
            "Callithrix jacchus",
            "Saimiri boliviensis",
            "Saguinus labiatus",
            "Macaca mulatta",
            "Macaca nemestrina",
            "Pygathrix bieti",
            "Papio hamadryas",
            "Microcebus murinus",
            "Daubentonia madagascariensis",
            "Otolemur garnettii",
            "Gorilla gorilla",
            "Homo sapiens",
            "Pan paniscus",
            "Pongo pygmaeus",
            "Pan troglodytes",
            "Symphalangus syndactylus",
            "Nomascus leucogenys",
            "Lemur catta",
            "Ornithorhynchus anatinus",
            "Cricetulus griseus",
            "Cavia porcellus",
            "Mus musculus",
            "Rattus norvegicus",
            "Bos taurus",
            "Capra hircus",
            "Ovis aries",
            "Tupaia chinensis",
            "Sus scrofa",
            "Anolis carolinensis",
            "Alligator mississippiensis",
            "Chrysemys picta",
            "Ophiophagus hannah",
            "Python bivittatus",
            "Astatotilapia burtoni",
            "Carassius auratus",
            "Cyprinus carpio",
            "Danio rerio",
            "Electrophorus electricus",
            "Fugu rubripes",
            "Gadus morhua",
            "Hippoglossus hippoglossus",
            "Ictalurus punctatus",
            "Metriaclima zebra",
            "Neolamprologus brichardi",
            "Nothobranchius furzeri",
            "Oryzias latipes",
            "Oncorhynchus mykiss",
            "Oreochromis niloticus",
            "Pundamilia nyererei",
            "Paralichthys olivaceus",
            "Salmo salar",
            "Tetraodon nigroviridis",
            "Lytechinus variegatus",
            "Patiria miniata",
            "Strongylocentrotus purpuratus",
            "Saccoglossus kowalevskii",
            "Ixodes scapularis",
            "Parasteatoda tepidariorum",
            "Rhipicephalus microplus",
            "Tetranychus urticae",
            "Daphnia pulex",
            "Marsupenaeus japonicus",
            "Triops cancriformis",
            "Aedes aegypti",
            "Anopheles gambiae",
            "Aphis gossypii",
            "Apis mellifera",
            "Acyrthosiphon pisum",
            "Bactrocera dorsalis",
            "Biston betularia",
            "Bombyx mori",
            "Culex quinquefasciatus",
            "Drosophila ananassae",
            "Drosophila erecta",
            "Drosophila grimshawi",
            "Drosophila melanogaster",
            "Drosophila mojavensis",
            "Drosophila persimilis",
            "Drosophila pseudoobscura",
            "Dinoponera quadriceps",
            "Drosophila sechellia",
            "Drosophila simulans",
            "Drosophila virilis",
            "Drosophila willistoni",
            "Drosophila yakuba",
            "Heliconius melpomene",
            "Locusta migratoria",
            "Mayetiola destructor",
            "Manduca sexta",
            "Nasonia giraulti",
            "Nasonia longicornis",
            "Nasonia vitripennis",
            "Polistes canadensis",
            "Plutella xylostella",
            "Spodoptera frugiperda",
            "Tribolium castaneum",
            "Strigamia maritima",
            "Ascaris suum",
            "Brugia malayi",
            "Brugia pahangi",
            "Caenorhabditis brenneri",
            "Caenorhabditis briggsae",
            "Caenorhabditis elegans",
            "Caenorhabditis remanei",
            "Haemonchus contortus",
            "Heligmosomoides polygyrus",
            "Pristionchus pacificus",
            "Panagrellus redivivus",
            "Strongyloides ratti",
            "Capitella teleta",
            "Glottidia pyramidata",
            "Terebratulina retusa",
            "Haliotis rufescens",
            "Lottia gigantea",
            "Melibe leonina",
            "Cerebratulus lacteus",
            "Echinococcus granulosus",
            "Echinococcus multilocularis",
            "Fasciola hepatica",
            "Gyrodactylus salaris",
            "Mesocestoides corti",
            "Schistosoma japonicum",
            "Schistosoma mansoni",
            "Schmidtea mediterranea",
            "Aiptasia pallida",
            "Hydra magnipapillata",
            "Nematostella vectensis",
            "Amphimedon queenslandica",
            "Leucosolenia complicata",
            "Sycon ciliatum"
        ]

        for entry in split_txt:
            if len(entry) > 0:
                split_entry = entry.split(" ")
                organism = split_entry[2] + " " + split_entry[3]

                if organism in metazoaFamilies:
                    pre_mir_name = split_entry[0]
                    organisms.append(organism)
                    preMirName.append(pre_mir_name)
                    preMirSeq.append(split_entry[-1].replace("\n", '').replace('stem-loop', ''))

                    # init 5p 3p
                    entry_five_p = pname_to_data.get(pre_mir_name.lower() + "-5p", None)
                    entry_three_p = pname_to_data.get(pre_mir_name + "-3p", None)

                    self.pre_mir_name_to_seeds_map[pre_mir_name] = {}
                    self.pre_mir_name_to_mature_5p_or_3p_map[pre_mir_name] = {}

                    if entry_five_p is not None:
                        name, seq, seed = init_p(entry_five_p, self.seed_length)
                        self.pre_mir_name_to_seeds_map[pre_mir_name][seed] = entry_five_p

                        mature = Mature(pre_mir_name, name, "5p", seed)
                        self.pre_mir_name_to_mature_5p_or_3p_map[pre_mir_name]["5p"] = mature
                    else:
                        name, seq, seed = None, None, None

                    fivePMatureMirName.append(name)
                    fivePMatureMirSeq.append(seq)
                    fivePMatureMirSeed.append(seed)

                    if entry_three_p is not None:
                        name, seq, seed = init_p(entry_three_p, self.seed_length)
                        self.pre_mir_name_to_seeds_map[pre_mir_name][seed] = entry_three_p

                        mature = Mature(pre_mir_name, name, "3p", seed)
                        self.pre_mir_name_to_mature_5p_or_3p_map[pre_mir_name]["3p"] = mature
                    else:
                        name, seq, seed = None, None, None

                    threePMatureMirName.append(name)
                    threePMatureMirSeq.append(seq)
                    threePMatureMirSeed.append(seed)

        data = np.array([preMirName,
                         organisms,
                         preMirSeq,
                         fivePMatureMirName,
                         fivePMatureMirSeq,
                         fivePMatureMirSeed,
                         threePMatureMirName,
                         threePMatureMirSeq,
                         threePMatureMirSeed])

        # export_table_to_csv([preMirName,
        #                      organisms,
        #                      preMirSeq,
        #                      fivePMatureMirName,
        #                      fivePMatureMirSeq,
        #                      fivePMatureMirSeed,
        #                      threePMatureMirName,
        #                      threePMatureMirSeq,
        #                      threePMatureMirSeed])

        return data

    def find_common_prefix(self, mature_name_list):
        mature_name_appearances_map = defaultdict(int)

        for mature_name in mature_name_list:
            mature_name_appearances_map[mature_name] += 1

        try:
            common_prefix = max(mature_name_appearances_map.items(), key=operator.itemgetter(1))[0]
            if commonprefix is not None and len(common_prefix) != 0:
                return common_prefix
        except:
            pass

    def reconstruct_mature_name(self, mature_name):
        mature_name_without_prefix = mature_name.split("-", 1)[1].lower()
        mature_name_split_arr = mature_name_without_prefix.split('-')
        #if mature_name_split_arr[0] == 'mir' and (mature_name_split_arr[2] == '5p' or mature_name_split_arr[2] == '3p'):
        name = self.remove_letters_from_string(mature_name_split_arr[1])
        mir = ''
        threeP_fiveP = ''
        if len(mature_name_split_arr) >= 1:
            mir = mature_name_split_arr[0] + '-'
        if len(mature_name_split_arr) >= 3:
            threeP_fiveP = '-' + mature_name_split_arr[2]
        mature_name_reconstructed = mir + \
                                    str(name) + \
                                    threeP_fiveP
        return mature_name_reconstructed

    # two-way mapping between a seed and a mature mir name
    def create_seed_mature_name_map_file(self):
        seed_to_mature_map = {}
        mature_to_seed_map = {}

        for seed in self.seed_list:
            seed_dict = map_seed_to_organisms_extended(
                self.table_data,
                seed,
                self.organisms,
                self.pre_mir_name_to_seeds_map,
                self.pre_mir_name_to_mature_5p_or_3p_map)

            # mature_name_appearances_map = defaultdict(int)
            mature_name_list = []
            for organism in seed_dict[seed]:
                for pre_mir_name in seed_dict[seed][organism]:
                    mature_name = seed_dict[seed][organism][pre_mir_name]['mature name']
                    mature_name_reconstructed = self.reconstruct_mature_name(mature_name)
                    if mature_name_reconstructed is not None and len(mature_name_reconstructed) != 0:
                        mature_name_list.append(mature_name_reconstructed)
                    # mature_name_appearances_map[mature_name_filtered] += 1

            common_prefix = self.find_common_prefix(mature_name_list)
            if common_prefix is not None or len(str(common_prefix)) != 0:
                seed_to_mature_map[seed] = common_prefix
                mature_to_seed_map[common_prefix] = seed

        with open('maps/seed_to_mature_map_' + str(self.seed_length) + '.txt', "w") as f:
            json.dump(seed_to_mature_map, f, indent=4)
        with open('maps/mature_to_seed_map_' + str(self.seed_length) + '.txt', "w") as f:
            json.dump(mature_to_seed_map, f, indent=4)

    def remove_letters_from_string(self, string):
        for letter in string:
            if letter.isalpha():
                string = string.replace(letter, '')
        return string

    def init_seed_mature_name_map(self):
        with open('static/Model/maps/seed_to_mature_map_' + str(self.seed_length) + '.txt', 'rb') as fp:
            seed_to_mature_map = json.load(fp)

        return seed_to_mature_map

    def init_mature_name_seed_map(self):
        with open('static/Model/maps/mature_to_seed_map_' + str(self.seed_length) + '.txt', 'rb') as fp:
            mature_to_seed_map = json.load(fp)

        return mature_to_seed_map
