import numpy as np

import data
import json
import reader


def main():
    table_data = data.table_from_txt_file("hairpin.txt", 6)
    seed_list = reader.get_all_seed(table_data)
    pre_mir_name_to_seeds_map = data.pre_mir_name_to_seeds_map
    organisms = np.unique(table_data[1])

    # random chosen seed...
    chosen_seed = seed_list[123]

    seed_dict = reader.map_seed_to_organisms_extended(
                                          table_data,
                                          chosen_seed,
                                          organisms,
                                          pre_mir_name_to_seeds_map,
                                          data.pre_mir_name_to_mature_5p_or_3p_map)

    reader.create_seed_json(chosen_seed, seed_dict)


if __name__ == "__main__":
    main()
