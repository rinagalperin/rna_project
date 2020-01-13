import json
from collections import defaultdict
from os.path import commonprefix
import numpy as np
import operator

from static.Model import mapper
from static.Model.mature import Mature
from static.Model.mapper import create_map_5p_3p, init_p, get_all_seed, map_seed_to_organisms_extended


def table_from_txt_file(path_input, seed_length, pre_mir_name_to_seeds_map, pre_mir_name_to_mature_5p_or_3p_map):
    """
        Creates database from original FASTA files
        """
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

            # filter organisms not from Metazoa family of organisms
            if organism in metazoaFamilies:
                pre_mir_name = split_entry[0].lower()
                pre_mir_sequence = split_entry[-1].replace("\n", '').replace('stem-loop', '')

                organisms.append(organism)
                preMirName.append(pre_mir_name)
                preMirSeq.append(pre_mir_sequence)

                # init 5p 3p
                entry_five_p = pname_to_data.get(pre_mir_name + '-5p', None)
                entry_three_p = pname_to_data.get(pre_mir_name + '-3p', None)

                # if the entry doesn't explicitly states '3p' or '5p', check the sub-sequence
                # location in the full pre-mir sequence to determine its type (using function find_three_or_five_p)
                if entry_three_p is None or entry_five_p is None:
                    general_entry = pname_to_data.get(pre_mir_name, None)
                    if general_entry is not None:
                        if find_three_or_five_p(general_entry, pre_mir_sequence) == '3p':
                            entry_three_p = general_entry
                        elif find_three_or_five_p(general_entry, pre_mir_sequence) == '5p':
                            entry_five_p = general_entry

                pre_mir_name_to_seeds_map[pre_mir_name] = {}
                pre_mir_name_to_mature_5p_or_3p_map[pre_mir_name] = {}

                # handle 5p sub-sequence of pre-mir
                if entry_five_p is not None:
                    name, seq, seed = init_p(entry_five_p, seed_length)
                    if name is not None and '5p' not in name:
                        name = name + '-5p'
                    pre_mir_name_to_seeds_map[pre_mir_name][seed] = entry_five_p

                    mature = Mature(pre_mir_name, name, "5p", seed)
                    pre_mir_name_to_mature_5p_or_3p_map[pre_mir_name]["5p"] = mature
                else:
                    name, seq, seed = None, None, None

                fivePMatureMirName.append(name)
                fivePMatureMirSeq.append(seq)
                fivePMatureMirSeed.append(seed)

                # handle 3p sub-sequence of pre-mir
                if entry_three_p is not None:
                    name, seq, seed = init_p(entry_three_p, seed_length)
                    if name is not None and '3p' not in name:
                        name = name + '-3p'
                    pre_mir_name_to_seeds_map[pre_mir_name][seed] = entry_three_p

                    mature = Mature(pre_mir_name, name, "3p", seed)
                    pre_mir_name_to_mature_5p_or_3p_map[pre_mir_name]["3p"] = mature
                else:
                    name, seq, seed = None, None, None

                threePMatureMirName.append(name)
                threePMatureMirSeq.append(seq)
                threePMatureMirSeed.append(seed)

    # completed database construction
    data = np.array([preMirName,
                     organisms,
                     preMirSeq,
                     fivePMatureMirName,
                     fivePMatureMirSeq,
                     fivePMatureMirSeed,
                     threePMatureMirName,
                     threePMatureMirSeq,
                     threePMatureMirSeed])

    return data


def find_common_prefix(mature_names_list):
    mature_name_appearances_map = defaultdict(int)

    for mature_name in mature_names_list:
        mature_name_appearances_map[mature_name] = mature_name_appearances_map.get(mature_name, 0) + 1

    try:
        common_prefix = max(mature_name_appearances_map.items(), key=operator.itemgetter(1))[0]
        if commonprefix is not None and len(common_prefix) != 0:
            return common_prefix
    except:
        pass


def reconstruct_mature_name(mature_name):
    """
        Reconstructs a mature miRNA name to be able to compare all mature names and
        choose one representative name for the entire family
        """

    # for example: ppy-miR-548e -> we get: ['ppy', 'mir-548e']. note we split once by '-'.
    # result: mature_name_without_prefix = mir-548e
    mature_name_without_prefix = mature_name.split("-", 1)[1].lower()
    mature_name_split_arr = ''
    mir = ''
    name = ''

    # remove prefix
    if len(mature_name_without_prefix) > 0 and '-' in mature_name_without_prefix:
        # ['mir', '548e']
        mature_name_split_arr = mature_name_without_prefix.split('-')
    else:
        print("error in removing prefix - with name " + mature_name_without_prefix)

    # get the prefix (mir/let/..) and remove redundant letters from the name
    if len(mature_name_split_arr) > 1:
        mir = mature_name_split_arr[0] + '-'
        # 548e -> 548
        name = remove_letters_from_string(mature_name_split_arr[1])
        # TODO: remove?
        if len(name) == 0:
            name = mature_name_split_arr[1]

    else:
        print("error in removing letters - with name " + mature_name_without_prefix)

    threeP_fiveP = ''
    if len(mature_name_split_arr) >= 3:
        # add the rest of the name if exists (for example, in: mir-9-3-3p the name will change from '9' to '9-3')
        name_remainder = mature_name_split_arr[2:-1]
        if len(name_remainder) > 0:
            if len(name) == 0:
                name = '-'.join(name_remainder)
            else:
                name += '-'+'-'.join(name_remainder)

        # add the 3p/5p suffix
        threeP_fiveP = '-' + mature_name_split_arr[-1]

    if len(name) != 0:
        mature_name_reconstructed = mir + \
                                    str(name) + \
                                    threeP_fiveP

        return mature_name_reconstructed

    return None


def create_seed_mature_name_map_file(seed_list, seed_length, pre_mir_name_to_mature_5p_or_3p_map, pre_mir_name_to_seeds_map):
    """
        two-way mapping between a seed and a mature mir name.
        creates actual database files.
        """
    seed_to_mature_map = {}

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
        mature_names_list = []
        for organism in seed_dict[seed]:
            for pre_mir_name in seed_dict[seed][organism]:
                mature_name = seed_dict[seed][organism][pre_mir_name]['mature name']
                # reconstruct mature name: remove prefix, remove letters from mid name, etc.
                mature_name_reconstructed = reconstruct_mature_name(mature_name)
                if mature_name_reconstructed is not None and len(mature_name_reconstructed) != 0:
                    # collect all reconstructed names to later chose one family name representative from
                    mature_names_list.append(mature_name_reconstructed)

        # decide on the chosen family name using majority vote selection
        common_prefix = find_common_prefix(mature_names_list)
        if common_prefix is not None and len(str(common_prefix)) != 0:
            seed_to_mature_map[seed] = common_prefix
            print("done with seed " + str(seed) + " and mapped to " + str(common_prefix))

    # access to database and save file
    with open('static/Model/maps/seed_to_mature_map_' + str(seed_length) + '.txt', "w") as f:
        json.dump(seed_to_mature_map, f, indent=4)


def create_mature_name_seed_map_file(seed_length,
                                     table_data,
                                     organisms,
                                     pre_mir_name_to_seeds_map,
                                     pre_mir_name_to_mature_5p_or_3p_map):
    mature_to_seed_map = {}

    # load seed-to-mature dict
    with open('static/Model/maps/seed_to_mature_map_' + str(seed_length) + '.txt', 'rb') as fp:
        seed_mature_name_map = json.load(fp)

    # since different seeds could be mapped to the same family name, we want to first collect all the unique family
    # names and then evaluate their most dominant seed representative
    family_names = np.unique(list(seed_mature_name_map.values()))

    # for each family name we want to find the most dominant seed sequence
    for family_name in family_names:
        most_dominant_seed = ''
        most_dominant_seed_dict = {}
        family_name_seeds = []

        # collect all the seeds that are mapped to the current family name
        for seed, fn in seed_mature_name_map.items():
            if fn == family_name:
                family_name_seeds.append(seed)

        # go over these seeds and get the most dominant one tor represent the family
        for seed in family_name_seeds:
            curr_seed_dict = mapper.map_seed_to_organisms_extended(table_data,
                                                                   seed,
                                                                   organisms,
                                                                   pre_mir_name_to_seeds_map,
                                                                   pre_mir_name_to_mature_5p_or_3p_map)

            # update largest dict for the family name
            curr_size = sum(len(v) for v in curr_seed_dict.values())
            prev_size = sum(len(v) for v in most_dominant_seed_dict.values())
            if curr_size > prev_size:
                most_dominant_seed = seed

        # set the map value for the family name
        mature_to_seed_map[family_name] = most_dominant_seed
        print("done with family name " + family_name + " and mapped to " + most_dominant_seed)

    # save to file
    with open('static/Model/maps/mature_to_seed_map_' + str(seed_length) + '.txt', "w") as f:
        json.dump(mature_to_seed_map, f, indent=4)


def remove_letters_from_string(string):
    """
        helper function to remove letters from mature name middle part.
        :returns original string after letter removal
        """
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


def find_str(full_string, sub_string):
    """
        :returns the *end* index of sub_string's first appearance in full_string
        for example: find_str("Happy birthday", "py") will return: 4
        """
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
    """
        Determine whether an entry is of type 3p or 5p according to its location in the pre-mir sequence
        :returns '3p' or '5p'
        """
    if unknown_p_entry is not None:
        entry_three_p_seq = unknown_p_entry[-1:]
        lines = entry_three_p_seq[0].splitlines()

        if len(lines) == 2:
            sub_sequence = lines[1]
            end_index_of_sub_in_full = find_str(pre_mir_sequence, sub_sequence)
            # left half -> 5p
            if end_index_of_sub_in_full <= len(pre_mir_sequence) / 2:
                return '5p'
            # right half -> 3p
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
#create_seed_mature_name_map_file(seed_list_6, 6, pre_mir_name_to_mature_5p_or_3p_map_6, pre_mir_name_to_seeds_map_6)
#create_mature_name_seed_map_file(6,
#                                 table_data_6,
#                                 organisms_6,
#                                 pre_mir_name_to_seeds_map_6,
#                                 pre_mir_name_to_mature_5p_or_3p_map_6)
#create_seed_mature_name_map_file(seed_list_7, 7, pre_mir_name_to_mature_5p_or_3p_map_7, pre_mir_name_to_seeds_map_7)
#create_mature_name_seed_map_file(7,
#                                 table_data_7,
#                                 organisms_7,
#                                 pre_mir_name_to_seeds_map_7,
#                                 pre_mir_name_to_mature_5p_or_3p_map_7)
##########################################

seed_mature_name_map_6 = init_seed_mature_name_map(6)
seed_mature_name_map_7 = init_seed_mature_name_map(7)

mature_name_seed_map_6 = init_mature_name_seed_map(6)
mature_name_seed_map_7 = init_mature_name_seed_map(7)
