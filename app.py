from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', data={})


@app.route('/get_data/<input>')
def get_data(input):
    data = {"url": input}
    return json.dumps(data)

@app.route('/info')
def info():
    return render_template('info.html', data={})

@app.route('/reports')
def reports():
    return render_template('reports.html', data={})

if __name__ == '__main__':
    app.run(debug=True)
