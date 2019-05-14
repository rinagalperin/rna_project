import json
from collections import defaultdict
from os.path import commonprefix
import numpy as np
import operator

from static.Model.mature import Mature
from static.Model.mapper import create_map_5p_3p, init_p, get_all_seed, map_seed_to_organisms_extended, \
    export_table_to_csv


def table_from_txt_file(path_input, seed_length, pre_mir_name_to_seeds_map, pre_mir_name_to_mature_5p_or_3p_map):
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
        "Canis familiaris",
        "Dasypus novemcinctus",
        "Oryctolagus cuniculus",
        "Artibeus jamaicensis",
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
        "Cyprinus carpio",
        "Danio rerio",
        "Electrophorus electricus",
        "Fugu rubripes",
        "Gadus morhua",
        "Hippoglossus hippoglossus",
        "Ictalurus punctatus",
        "Metriaclima zebra",
        "Neolamprologus brichardi",
        "Oryzias latipes",
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
        "Hydra magnipapillata",
        "Nematostella vectensis",
        "Amphimedon queenslandica",
        "Leucosolenia complicata",
        "Sycon ciliatum",
        "Dictyostelium discoideum"
    ]

    for entry in split_txt:
        if len(entry) > 0:
            split_entry = entry.split(" ")
            organism = split_entry[2] + " " + split_entry[3]

            if organism in metazoaFamilies:
                pre_mir_name = split_entry[0].lower()
                pre_mir_sequence = split_entry[-1].replace("\n", '').replace('stem-loop', '')

                organisms.append(organism)
                preMirName.append(pre_mir_name)
                preMirSeq.append(pre_mir_sequence)

                # init 5p 3p
                entry_five_p = pname_to_data.get(pre_mir_name + '-5p', None)
                entry_three_p = pname_to_data.get(pre_mir_name + '-3p', None)

                # if the entry doesn't explicitly states '3p' or '5p'
                if entry_three_p is None or entry_five_p is None:
                    general_entry = pname_to_data.get(pre_mir_name, None)
                    if general_entry is not None:
                        if find_three_or_five_p(general_entry, pre_mir_sequence) == '3p':
                            entry_three_p = general_entry
                        elif find_three_or_five_p(general_entry, pre_mir_sequence) == '5p':
                            entry_five_p = general_entry

                pre_mir_name_to_seeds_map[pre_mir_name] = {}
                pre_mir_name_to_mature_5p_or_3p_map[pre_mir_name] = {}

                if entry_five_p is not None:
                    name, seq, seed = init_p(entry_five_p, seed_length)
                    pre_mir_name_to_seeds_map[pre_mir_name][seed] = entry_five_p

                    mature = Mature(pre_mir_name, name, "5p", seed)
                    pre_mir_name_to_mature_5p_or_3p_map[pre_mir_name]["5p"] = mature
                else:
                    name, seq, seed = None, None, None

                fivePMatureMirName.append(name)
                fivePMatureMirSeq.append(seq)
                fivePMatureMirSeed.append(seed)

                if entry_three_p is not None:
                    name, seq, seed = init_p(entry_three_p, seed_length)
                    pre_mir_name_to_seeds_map[pre_mir_name][seed] = entry_three_p

                    mature = Mature(pre_mir_name, name, "3p", seed)
                    pre_mir_name_to_mature_5p_or_3p_map[pre_mir_name]["3p"] = mature
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

    ##########################################
    # export_table_to_csv([preMirName,
    #                      organisms,
    #                      preMirSeq,
    #                      fivePMatureMirName,
    #                      fivePMatureMirSeq,
    #                      fivePMatureMirSeed,
    #                      threePMatureMirName,
    #                      threePMatureMirSeq,
    #                      threePMatureMirSeed])
    ##########################################

    return data


def find_common_prefix(mature_name_list):
    mature_name_appearances_map = defaultdict(int)

    for mature_name in mature_name_list:
        mature_name_appearances_map[mature_name] += 1

    try:
        common_prefix = max(mature_name_appearances_map.items(), key=operator.itemgetter(1))[0]
        if commonprefix is not None and len(common_prefix) != 0:
            return common_prefix
    except:
        pass


def reconstruct_mature_name(mature_name):
    mature_name_without_prefix = mature_name.split("-", 1)[1].lower()
    mature_name_split_arr = mature_name_without_prefix.split('-')
    # if mature_name_split_arr[0] == 'mir' and (mature_name_split_arr[2] == '5p' or mature_name_split_arr[2] == '3p'):
    name = remove_letters_from_string(mature_name_split_arr[1])
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
def create_seed_mature_name_map_file(seed_list, seed_length, pre_mir_name_to_mature_5p_or_3p_map, pre_mir_name_to_seeds_map):
    seed_to_mature_map = {}
    mature_to_seed_map = {}

    if seed_length == 6:
        table_data = table_data_6
        organisms = organisms_6
    else:
        table_data = table_data_7
        organisms = organisms_7

    for seed in seed_list:
        seed_dict = map_seed_to_organisms_extended(
            table_data,
            seed,
            organisms,
            pre_mir_name_to_seeds_map,
            pre_mir_name_to_mature_5p_or_3p_map)

        # mature_name_appearances_map = defaultdict(int)
        mature_name_list = []
        for organism in seed_dict[seed]:
            for pre_mir_name in seed_dict[seed][organism]:
                mature_name = seed_dict[seed][organism][pre_mir_name]['mature name']
                mature_name_reconstructed = reconstruct_mature_name(mature_name)
                if mature_name_reconstructed is not None and len(mature_name_reconstructed) != 0:
                    mature_name_list.append(mature_name_reconstructed)
                # mature_name_appearances_map[mature_name_filtered] += 1

        common_prefix = find_common_prefix(mature_name_list)
        if common_prefix is not None or len(str(common_prefix)) != 0:
            seed_to_mature_map[seed] = common_prefix
            mature_to_seed_map[common_prefix] = seed
            # print("done with entry " + str(len(seed_to_mature_map)))

    with open('static/Model/maps/seed_to_mature_map_' + str(seed_length) + '.txt', "w") as f:
        json.dump(seed_to_mature_map, f, indent=4)
    with open('static/Model/maps/mature_to_seed_map_' + str(seed_length) + '.txt', "w") as f:
        json.dump(mature_to_seed_map, f, indent=4)


def remove_letters_from_string(string):
    for letter in string:
        if letter.isalpha():
            string = string.replace(letter, '')
    return string


def init_seed_mature_name_map(seed_length):
    with open('static/Model/maps/seed_to_mature_map_' + str(seed_length) + '.txt', 'rb') as fp:
        seed_to_mature_map = json.load(fp)

    return seed_to_mature_map


def init_mature_name_seed_map(seed_length):
    with open('static/Model/maps/mature_to_seed_map_' + str(seed_length) + '.txt', 'rb') as fp:
        mature_to_seed_map = json.load(fp)

    return mature_to_seed_map


# return the *end* index of sub_string's first appearance in full_string
# for example: find_str("Happy birthday", "py") will return: 4
def find_str(full_string, sub_string):
    index = 0

    if sub_string in full_string:
        c = sub_string[0]
        for ch in full_string:
            if ch == c:
                if full_string[index:index + len(sub_string)] == sub_string:
                    return index + len(sub_string) - 1

            index += 1

    return -1


def find_three_or_five_p(unknown_p_entry, pre_mir_sequence):
    if unknown_p_entry is not None:
        entry_three_p_seq = unknown_p_entry[-1:]
        lines = entry_three_p_seq[0].splitlines()

        if len(lines) == 2:
            sub_sequence = lines[1]
            end_index_of_sub_in_full = find_str(pre_mir_sequence, sub_sequence)
            if end_index_of_sub_in_full <= len(pre_mir_sequence) / 2:
                return '5p'
            else:
                return '3p'
    return 'none'


# pre-mir-name: cin-mir-4074
# to ->
# seed: AACGUU
pre_mir_name_to_seeds_map_6 = {}
pre_mir_name_to_seeds_map_7 = {}

# pre-mir-name: cin-mir-4074
# to ->
# mature-name-and-type: {{cin-miR-4074-3p, 3p}}
pre_mir_name_to_mature_5p_or_3p_map_6 = {}
pre_mir_name_to_mature_5p_or_3p_map_7 = {}

table_data_6 = table_from_txt_file("static/Model/hairpin.txt", 6, pre_mir_name_to_seeds_map_6, pre_mir_name_to_mature_5p_or_3p_map_6)
table_data_7 = table_from_txt_file("static/Model/hairpin.txt", 7, pre_mir_name_to_seeds_map_7, pre_mir_name_to_mature_5p_or_3p_map_7)

seed_list_6 = get_all_seed(table_data_6)
seed_list_7 = get_all_seed(table_data_7)

organisms_6 = np.unique(table_data_6[1])
organisms_7 = np.unique(table_data_7[1])

###### create map files ##################
# create_seed_mature_name_map_file(seed_list_6, 6, pre_mir_name_to_mature_5p_or_3p_map_6, pre_mir_name_to_seeds_map_6)
# create_seed_mature_name_map_file(seed_list_7, 7, pre_mir_name_to_mature_5p_or_3p_map_7, pre_mir_name_to_seeds_map_7)
##########################################

seed_mature_name_map_6 = init_seed_mature_name_map(6)
seed_mature_name_map_7 = init_seed_mature_name_map(7)

mature_name_seed_map_6 = init_mature_name_seed_map(6)
mature_name_seed_map_7 = init_mature_name_seed_map(7)
