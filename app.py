from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import os.path
import json
from jsgn import jsgn

app = Flask(__name__)

graph_file_name = "graph.json"

dg = jsgn.open_graph(graph_file_name)

def save():
    jsgn.save_graph(dg, graph_file_name)    

@app.route("/")
def index():
    return render_template('index.html', nodes=dg.get_nodes())

@app.route("/graph")
def graph():
    return dg.dump()

@app.route("/node/<nodeid>", methods=['GET', 'PUT','DELETE'])
def node(nodeid):
    if request.method == 'PUT':
        nodeid = request.values['id']
        ## currently overwrites.  Want?
        ## add metadata?
        node = dg.add_node(nodeid)
        save()
        url = url_for('node',nodeid=nodeid)
        return "{\"nodeid\": \"%s\",\"url\": \"%s\"}" % (nodeid, url)
    elif request.method == 'DELETE':
        dg.remove_node(nodeid)
        save()
        return "{}"
    else:
        if dg.has_node(nodeid):
            return render_template('node.html', node=dg.get_node(nodeid))
        else:
            return render_template('new_node.html', nodeid=nodeid)

if __name__ == "__main__":
    app.run()
