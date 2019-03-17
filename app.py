from flask import Flask, render_template
import json
import numpy as np

from static.Model import data, mapper

app = Flask(__name__)
seed_length = 6


@app.route('/')
def hello_world():
    return render_template('index.html', data={})


@app.route('/get_data/<chosen_seed>')
def get_data(chosen_seed):
    # user's input seed
    #chosen_seed = {"url": input}
    seed_length = len(chosen_seed)

    my_data = data.Data(seed_length)

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
    return json.dumps(seed_dict)


@app.route('/info')
def info():
    return render_template('info.html', data={})


@app.route('/nav.html')
def nav():
    return render_template('nav.html', data={})


@app.route('/reports')
def reports():
    return render_template('reports.html', data={})


@app.route('/contact')
def contact():
    return render_template('contact.html', data={})


if __name__ == '__main__':
    app.run(debug=True)
