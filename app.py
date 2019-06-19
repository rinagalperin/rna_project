import json
import re
import numpy as np
from collections import defaultdict

from flask import Flask, render_template

from static.Model import data, mapper, tree_creator

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', data={})


@app.route('/get_data/<user_input>')
def get_data(user_input):
    if '-' in user_input:
        # default seed length in case user enters a family name
        # instead of a seed sequence
        seed_length = 6
    else:
        seed_length = len(user_input)

    # illegal seed sequence length
    if seed_length != 6 and seed_length != 7:
        return '-1'

    # turn to the relevant databse given the user's input seed length
    if seed_length == 6:
        mature_name_seed_map = data.mature_name_seed_map_6
        seed_mature_name_map = data.seed_mature_name_map_6
        table_data = data.table_data_6
        pre_mir_name_to_seeds_map = data.pre_mir_name_to_seeds_map_6
        organisms = data.organisms_6
        pre_mir_name_to_mature_5p_or_3p_map = data.pre_mir_name_to_mature_5p_or_3p_map_6
    else:
        mature_name_seed_map = data.mature_name_seed_map_7
        seed_mature_name_map = data.seed_mature_name_map_7
        table_data = data.table_data_7
        pre_mir_name_to_seeds_map = data.pre_mir_name_to_seeds_map_7
        organisms = data.organisms_7
        pre_mir_name_to_mature_5p_or_3p_map = data.pre_mir_name_to_mature_5p_or_3p_map_7

    seed_or_family_name = ''

    if '-' in user_input:
        user_input = user_input.lower()
        if user_input not in mature_name_seed_map.keys():
            return '-1'
        chosen_seed = mature_name_seed_map[user_input]
        # user entered family name, so other name is the seed
        seed_or_family_name = chosen_seed
    else:
        # in case user enters the seed sequence in non-capital letters,
        # turn the input to all upper case.
        user_input = user_input.upper()
        if user_input not in seed_mature_name_map.keys():
            return '-1'
        chosen_seed = user_input
        # user entered seed sequence, so other name is the family name
        family_name = seed_mature_name_map[user_input]
        seed_or_family_name = family_name

    seed_dict = mapper.map_seed_to_organisms_extended(
        table_data,
        chosen_seed,
        organisms,
        pre_mir_name_to_seeds_map,
        pre_mir_name_to_mature_5p_or_3p_map)

    if len(seed_dict[chosen_seed]) == 0:
        return '-1'

    # mapper.create_seed_json(chosen_seed, seed_dict)
    json_result = json.dumps(seed_dict)

    # concatenate several results using the '$' separator
    return json_result + '$' + seed_or_family_name


@app.route('/json_to_csv/<json_input>')
def json_to_csv(json_input):
    #result = json_to_table_txt(json_input)
    print(json_input)

    return json_input

# HTML output
@app.route('/json_to_html/<json_input>')
def json_to_html(json_input):
    import codecs
    f = codecs.open('templates/tree.html', 'r')
    # base html tree
    base = f.read()

    json_dict = json.loads(json_input)
    seed = list(json_dict)[0]
    organisms = list(json_dict[seed])

    # go over each relevant organism and count the number of mature miRNA sequences in it that
    # contain the given seed
    for organism in organisms:
        matures = list(json_dict[seed][organism])
        num_of_3p = 0
        num_of_5p = 0
        for mature in matures:
            # mature_name = json_dict[seed][organism][mature]['mature name']
            mature_3p_or_5p = json_dict[seed][organism][mature]['mature 3p or 5p']
            if mature_3p_or_5p == '3p':
                num_of_3p += 1
            else:
                num_of_5p += 1

        # added information that is attached to all organisms with the given seed
        extra_info = '<span class=INFO3> [' + str(num_of_3p) + '-3p, ' + str(num_of_5p) + '-5p] </span>'
        result = re.search(organism+'(.*)</LI>', base)
        # for testing purposes
        if result is None:
            print(organism)
        else:
            original_line = result.group(1)
            base = base.replace(original_line, original_line + extra_info)

    return base


# FASTA output
@app.route('/json_to_fasta/<json_input>')
def json_to_fasta(json_input):
    # FASTA format:
    # > mature_name
    # mature_sequence

    result = ''
    json_dict = json.loads(json_input)

    seed = list(json_dict)[0]
    organisms = list(json_dict[seed])

    # go over all relevant miRNA matures and extract their full sequence for the
    # FASTA file output
    for organism in organisms:
        matures = list(json_dict[seed][organism])

        for mature in matures:
            mature_name = json_dict[seed][organism][mature]['mature name']

            # extract only the mature sequence from the database
            filter1 = data.table_data_6[3] == mature_name
            filter2 = data.table_data_6[6] == mature_name
            idx = np.logical_or(filter1, filter2)
            res = data.table_data_6[:, idx]

            # the given mature name is of type 5p
            if res[3] == mature_name:
                mature_sequence = res[4]
            # the given mature name is of type 3p
            elif res[6] == mature_name:
                mature_sequence = res[7]
            else:
                mature_sequence = 'error'

            # if it's the first entry in the file - don't start with new line. Otherwise - add new line first.
            if mature_sequence != None:
                # not first entry
                if result != '':
                    result = result + '\n>' + mature_name + '\n' + mature_sequence
                # first entry in result FASTA file
                else:
                    result = result + '>' + mature_name + '\n' + mature_sequence
            # for testing purposes
            else:
                print(mature_sequence)
                print(mature_name)
                print(res)
                print('--------------')

    return str(result[0])


# returns all relevant organisms to the user's entry, in abbreviation format.
@app.route('/json_to_tree/<json_input>')
def json_to_tree(json_input):
    json_dict = json.loads(json_input)
    seed = list(json_dict)[0]

    organisms = list(json_dict[seed])
    organism_num_of_matures = {}
    short_names_organisms = []

    # gather how many 3p mature sequences the organism has, and how many 5p.
    organism_three_p = defaultdict(int)
    organism_five_p = defaultdict(int)

    tree_builder = tree_creator.TreeCreator(json_input)

    # collect the abbreviations of each mature sequence and the number of matures for each organism
    for organism in organisms:
        short_name_organism = tree_builder.get_short_organism_name(organism)
        matures = list(json_dict[seed][organism])
        short_names_organisms.append(short_name_organism + str(len(matures)))
        organism_num_of_matures[organism] = len(matures)

        # for mature in matures:
        #     # mature_name = json_dict[seed][organism][mature]['mature name']
        #     mature_3p_or_5p = json_dict[seed][organism][mature]['mature 3p or 5p']
        #     if mature_3p_or_5p == '3p':
        #         organism_three_p[organism] += 1
        #     else:
        #         organism_five_p[organism] += 1

    # tree_builder = tree_creator.TreeCreator(json_input)
    # newick_result = tree_builder.newick

    return str(short_names_organisms).strip('[]')


# returns the full name of an organism, given its short name
@app.route('/get_organism_full_name/<short_name>')
def get_organism_full_name(short_name):
    organisms_code_names_path = 'static/Model/miRbase_codes_names.txt'
    map_1 = {}
    with open(organisms_code_names_path) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for code in content:
        s = code.split('	')
        map_1[s[0]] = s[1]

    result = str(map_1[short_name])

    return result

@app.route('/info')
def info():
    return render_template('info.html', data={})


@app.route('/nav.html')
def nav():
    return render_template('nav.html', data={})


@app.route('/examples')
def examples():
    return render_template('examples.html', data={})


@app.route('/publications')
def publications():
    return render_template('publications.html', data={})


@app.route('/contact')
def contact():
    return render_template('contact.html', data={})


def json_to_table_txt(json_input):
    res = json_input[0]

    return res


if __name__ == '__main__':
    app.run(debug=True)
