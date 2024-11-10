How to run the code:
unpack all files in the same directory and go to main.py, where you select which map you want to load

Maps:
complex - contains all paths, footways
simple - without footways
very simple - without footways and paths
the simpler the map, the fewer nodes and edges the graph has

Other cool features:
graph functionality is done using networkx package, which simplifies the implementation
apparently there exists a package to read a geojson file, so I am using it to quickly read the file
you can visualise your graph through matplotlib by using the GeoGraph.visualise() method, in the graph_reader file you
can also configure the colors and sizes of nodes, edges and edge labels

Problems:
many of the roads from the dataset do not have a speed limit, this
is because many roads in leiden are not meant for cars but for pedestrians
I make the speed limit 30 by default, but I think the algorithm should
calculate the time for the route for a pedestrian, as Leiden is a small city anyway