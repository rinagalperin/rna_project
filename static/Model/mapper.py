import json
import numpy as np
from astropy.table import Table
from collections import defaultdict


def create_map_5p_3p(path_input):
    with open(path_input, "r") as f:
        split_txt = f.read().split('>')
        pname_to_data = {}

        for entry in split_txt:
            if len(entry) > 0:
                split_entry = entry.split(" ")
                pname_to_data[split_entry[0].lower()] = split_entry

        return pname_to_data


def init_p(p, seed_length):
    name = p[0]
    seq = p[4].split("\n")[1]
    seed = seq[1:seed_length + 1]

    return name, seq, seed


def export_table_to_csv(data_list):
    table = Table(data_list, names=(
        'Pre Mir Name',
        'Organism',
        'Pre Mir Sequence',
        '5P Mature Mir Name',
        '5P MatureMir Sequence',
        '5P Mature Mir Seed',
        '3P Mature Mir Name',
        '3P Mature Mir Sequence',
        '3P Mature Mir Seed'))

    table.write('table.csv', format='csv', overwrite=True)


def get_all_seed(data):
    seed = np.append(data[5], data[8])
    # WARNING: do not change to: 'seed is not None'!
    seed = seed[seed != None]
    return np.unique(seed)


def get_organisms_with_seed(seed, organisms, data):
    organisms_with_seed = []
    for j, organism in enumerate(organisms):
        idx = data[1] == organism
        only_organism_data = data[:, idx]
        five_seed = only_organism_data[5] == seed
        three_seed = only_organism_data[8] == seed
        both_seed = np.logical_and(five_seed, three_seed)

        if sum(five_seed) + sum(three_seed) - sum(both_seed) != 0:
            organisms_with_seed.append(organism)

    return organisms_with_seed
    # get number of times the seed appeared in the organism family:
    # return (sum(five_seed) + sum(three_seed) - sum(both_seed)) / len(only_organism_data[0])
    # return 1 if (sum(five_seed) + sum(three_seed) - sum(both_seed)) != 0 else 0


# get input seed from user, and gathers all information on that seed
def map_seed_to_organisms_extended(
        data,
        seed,
        organisms,
        pre_mir_name_to_seeds_map,
        pre_mir_name_to_mature_5p_or_3p_map):

    # find the organisms who have the given seed
    organisms_with_seed = get_organisms_with_seed(seed, organisms, data)

    # for each organism found - gather all pre-mir names of the organism's members
    # who have that seed.
    # exaple: Caenorhabditis elegans --> [cel-let-7, cel-lin-4, cel-mir-1, ...]
    organism_to_pre_mir_names_map = map_organism_to_pre_mir_names(data)

    # exaple: Caenorhabditis elegans -->
    # {cel-let-7: (mature_name: cin-miR-4074-3p, three_p_or_five_p: 3p),
    # cel-lin-4: (mature_name: cin-miR-4077-5p, three_p_or_five_p: 5p),
    # ...}
    organism_to_pre_mirs_map = {}

    for organism in organisms_with_seed:
        # total members of the organism
        all_members_of_organism = organism_to_pre_mir_names_map[organism]

        # for each organism who has the given seed, we want to find the specific members
        # of the organism who have that seed.
        member_of_organism_with_seed_to_mature_obj_map = {}
        for member in all_members_of_organism:
            if seed in pre_mir_name_to_seeds_map[member].keys():
                mature_3p = pre_mir_name_to_mature_5p_or_3p_map[member].get("3p", None)
                mature_5p = pre_mir_name_to_mature_5p_or_3p_map[member].get("5p", None)

                mature_dict = {}
                if mature_3p is not None and mature_3p.seed == seed:
                    mature_dict["mature name"] = mature_3p.mature_name
                    mature_dict["mature 3p or 5p"] = mature_3p.threeP_or_fiveP
                    member_of_organism_with_seed_to_mature_obj_map[member] = mature_dict
                if mature_5p is not None and mature_5p.seed == seed:
                    mature_dict["mature name"] = mature_5p.mature_name
                    mature_dict["mature 3p or 5p"] = mature_5p.threeP_or_fiveP
                    member_of_organism_with_seed_to_mature_obj_map[member] = mature_dict

        organism_to_pre_mirs_map[organism] = member_of_organism_with_seed_to_mature_obj_map
    seed_dict = {seed: organism_to_pre_mirs_map}

    return seed_dict


def create_seed_json(seed, seed_dict):
    with open("seeds/" + seed + ".txt", "w") as f:
        json.dump(seed_dict, f, indent=4)


def map_organism_to_pre_mir_names(data):
    # for example: mapping Caenorhabditis elegans to {cel-let-7, cel-lin-4, cel-mir-1, ...}
    i = 0
    length = len(data[0])

    map = defaultdict(list)

    while i < length:
        map[data[1][i]].append(data[0][i])
        i += 1

    return map

