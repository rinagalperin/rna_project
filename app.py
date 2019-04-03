from flask import Flask, render_template
import json
import pandas as pd
from json2html import json2html

from static.Model import data, mapper, tree_creator, list_creator

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', data={})


@app.route('/get_data/<user_input>')
def get_data(user_input):
    if '-' in user_input:
        seed_length = 6
    else:
        seed_length = len(user_input)

    my_data = data.Data(seed_length)

    if '-' in user_input:
        chosen_seed = my_data.mature_name_seed_map[user_input]
    else:
        chosen_seed = user_input

    table_data = my_data.table_data
    seed_list = my_data.seed_list
    pre_mir_name_to_seeds_map = my_data.pre_mir_name_to_seeds_map
    organisms = my_data.organisms

    seed_dict = mapper.map_seed_to_organisms_extended(
        table_data,
        chosen_seed,
        organisms,
        pre_mir_name_to_seeds_map,
        my_data.pre_mir_name_to_mature_5p_or_3p_map)

    mapper.create_seed_json(chosen_seed, seed_dict)
    json_result = json.dumps(seed_dict)

    return json_result


@app.route('/json_to_csv/<json_input>')
def json_to_csv(json_input):
    result = json_to_table_txt(json_input)
    df = pd.read_fwf(result, 'results')
    df.to_csv('results-rina.csv')
    return df


@app.route('/json_to_html/<json_input>')
def json_to_html(json_input):
    table = json2html.convert(json=json_input)
    result = list_creator.table2list(table)
    return result


@app.route('/json_to_fasta/<json_input>')
def json_to_fasta(json_input):
    # json_dict = json.loads(json_input)
    #
    # seed = list(json_dict)[0]
    # organisms = list(json_dict[seed])
    # organism_num_of_matures = {}
    #
    # for organism in organisms:
    #     matures = list(json_dict[seed][organism])
    #     organism_num_of_matures[organism] = len(matures)
    #
    #     for mature in matures:
    #         mature_name = json_dict[seed][organism][mature]['mature name']
    #         mature_3p_or_5p = json_dict[seed][organism][mature]['mature 3p or 5p']
    #
    # tree_builder = tree_creator.TreeCreator(json_input)

    return 'Rina'


# returns basic newick format for tree rendering in JS
@app.route('/json_to_tree/<json_input>')
def json_to_tree(json_input):
    json_dict = json.loads(json_input)

    seed = list(json_dict)[0]
    organisms = list(json_dict[seed])
    organism_num_of_matures = {}

    for organism in organisms:
        matures = list(json_dict[seed][organism])
        organism_num_of_matures[organism] = len(matures)

        for mature in matures:
            mature_name = json_dict[seed][organism][mature]['mature name']
            mature_3p_or_5p = json_dict[seed][organism][mature]['mature 3p or 5p']

    tree_builder = tree_creator.TreeCreator(json_input)
    newick_result = tree_builder.newick

    return newick_result


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
