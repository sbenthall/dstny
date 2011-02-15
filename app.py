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
node_template_file_name = "node_template.json"

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
        ## use template to preload metadata fields
        file = open(node_template_file_name,"r")
        metadata = json.loads(file.read())
        node = dg.add_node(nodeid, **metadata)
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


@app.route("/node/<nodeid>/metadata/<key>", methods=['GET','POST','DELETE'])
def node_metadata(nodeid, key):
    node = dg.get_node(nodeid)

    if node is None:
        pass
    elif request.method == 'GET':
        if 'edit' in request.args or not key in node.metadata:
            return render_template('edit_metadata.html', node=node, key=key)
        else:
            return node.metadata[key]
    elif request.method == 'POST':
        node.metadata[key] = request.values['value']
        save()
        return "{}"
    elif request.method == 'DELETE':
        del node.metadata[key]
        save()
        return "{}"


@app.route("/edge/<from_node>/<to_node>", methods=['PUT','DELETE'])
def edge(from_node, to_node):
    if request.method == 'PUT':
        dg.add_edge(from_node, to_node);
        save()
        return "{}"
    elif request.method == 'DELETE':
        dg.remove_edge(from_node, to_node);
        save()
        return "{}"

if __name__ == "__main__":
    app.run()
