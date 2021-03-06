from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
import os.path
import json
from jsgn import jsgn
from flaskext.markdown import Markdown
from pygraphviz import AGraph

app = Flask(__name__)
Markdown(app)

graph_file_name = "graph.json"
node_template_file_name = "node_template.json"
graph_image_name = "graph.png"

dg = jsgn.open_graph(graph_file_name)

@app.template_filter()
def inorder(items,order):
    def cm(e1, e2):
        # inefficient
        e1_index = order.index(e1) if e1 in order else 1e308
        e2_index = order.index(e2) if e2 in order else 1e308
        return cmp(e1_index, e2_index)
    return sorted(items, cm, lambda i:i[0])


def draw_graph():
    G = AGraph(dg.edges, directed=True, rankdir="LR")
    G.draw(graph_image_name,prog="dot")
    image_file = open(graph_image_name)
    return image_file

def save():
    jsgn.save_graph(dg, graph_file_name)    

@app.route("/")
def index():
    return render_template('index.html', nodes=dg.get_nodes())

@app.route("/graph")
def graph():
    return dg.dump()

@app.route("/draw")
def draw():
    image_file = draw_graph()
    return Response(image_file, mimetype="png")

@app.route("/node/<nodeid>", methods=['GET', 'PUT','DELETE','POST'])
def node(nodeid):
    if request.method == 'PUT':
        nodeid = request.values['id']
        ## currently overwrites.  Want?
        node = add_node(nodeid)
        url = url_for('node',nodeid=nodeid)
        return "{\"nodeid\": \"%s\",\"url\": \"%s\"}" % (nodeid, url)
    elif request.method == 'DELETE':
        dg.remove_node(nodeid)
        save()
        return "{}"
    elif request.method == 'POST':
        if 'rename' in request.values:
            new_name = request.values['rename']
            old_node = dg.get_node(nodeid)
            # make node with new name and old metadata
            new_node = dg.add_node(new_name, **old_node.metadata)
            # add edges to new node that match the old nodes'
            for from_node, to_node, metadata in dg:
                # the from... edges
                if from_node == nodeid:
                    dg.add_edge(new_node.id, to_node, **metadata)
                # the to... edges
                if to_node == nodeid:
                    dg.add_edge(from_node, new_node.id, **metadata)
            # remove the old node
            dg.remove_node(nodeid)
            return "{}"
        pass
    else: # GET
        if dg.has_node(nodeid):
            return render_template('node.html', node=dg.get_node(nodeid))
        else:
            return render_template('new_node.html', nodeid=nodeid)

def add_node(nodeid):
    ## use template to preload metadata fields
    file = open(node_template_file_name,"r")
    metadata = json.loads(file.read())
    node = dg.add_node(nodeid, **metadata)
    save()
    return node
    

@app.route("/node/<nodeid>/metadata", methods=['GET'])
def node_metadata(nodeid):
    node = dg.get_node(nodeid)

    if node is None:
        pass
    elif request.method == 'GET':
        return json.dumps(node.metadata)

@app.route("/node/<nodeid>/metadata/<key>", methods=['GET','POST','DELETE'])
def node_metadata_item(nodeid, key):
    node = dg.get_node(nodeid)

    if node is None:
        pass
    elif request.method == 'GET':
        if 'edit' in request.args or not key in node.metadata:
            return render_template('edit_metadata.html', node=node, key=key)
        else:
            return json.dumps(node.metadata[key])
    elif request.method == 'POST':
        node.metadata[key] = json.loads(request.values['value'])
        save()
        return "{}"
    elif request.method == 'DELETE':
        del node.metadata[key]
        save()
        return "{}"


@app.route("/edge/<from_node>/<to_node>", methods=['PUT','DELETE'])
def edge(from_node, to_node):
    if request.method == 'PUT':
        if not dg.has_node(from_node):
            add_node(from_node)
        if not dg.has_node(to_node):
            add_node(to_node)
        dg.add_edge(from_node, to_node);
        save()
        return "{}"
    elif request.method == 'DELETE':
        dg.remove_edge(from_node, to_node);
        save()
        return "{}"

if __name__ == "__main__":
    app.run()
