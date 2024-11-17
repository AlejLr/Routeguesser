How to run the code:
unpack all files in the same directory and go to main.py, where you select which map you want to load

Maps:
complex - contains all paths, footways
simple - without footways
very simple - without footways and paths
the simpler the map, the fewer nodes and edges the graph has

File_cleaner:
The original map file, stored as geojson, contains many unnecessary features
For speed up, but also mostly for consultation ease, the 'file_cleaner.py' file cleans this file, and returns a
json that contains only what the final Graph will contain, already labelled as in the final structure.
This is a one-time-function, and its product (out_file) is the json file that Map reads, NOT THE GEOJSON

Graph creation (_create_graph inside Map):
As the cleaned file is already structured as the final Graph (made using NetworkX), the reading functions is small and
immediate, and as such it is directly inserted into Maps, while the previous 'graph_reader' is no longer in use.
N.B: right now the coordinates that described the roads are not turned into tuples as the nodes, but this can be changed
 any time

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