from sklearn.tree import export_graphviz
import os
import pydot
import random
def tvisual(depth,columns,tree)->None:
    dot = export_graphviz(tree,
                    feature_names=columns,
                    filled=True,
                    rounded=True,max_depth = depth)
    dot_file_path = 'tree.dot'
    with open(dot_file_path, 'w') as dot_file:
        dot_file.write(dot)

    os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'


    (graph,) = pydot.graph_from_dot_file('tree.dot')
    graph.set_size('"2500,5000"')
    graph.set_dpi(50)
    graph.set_bgcolor('"#d4c6a1"')
    rndom_filename = str(random.randint(1,200000))+'.png'
    graph.write_png(rndom_filename)

