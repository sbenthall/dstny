from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import os.path
import json
from jsgn import jsgn

app = Flask(__name__)

dg = jsgn.open_graph("graph.json")


@app.route("/")
def index():
    return render_template('index.html', nodes=dg.as_dict()['nodes'].keys())

@app.route("/<nodeid>")
def node(nodeid):
    if dg.has_node(nodeid):
        return render_template('node.html', node=dg.get_node(nodeid))
    else:
        return render_template('new_node.html', nodeid=nodeid)

if __name__ == "__main__":
    app.run()
