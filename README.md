# BGPonGraph

This is a python program that creates a Promela file simulating the Boarder Gateway Protocol Algorithm on a graph.

How to run:
python3.7 creator.py [example_number] [number_nodes]

example_number can be:
    0 to read a graph from a file
    1, 2, ... for example graphs
        current example graphs:
            1 for two nodes connected to each other and the root
            2 for the classic graph of 3 nodes connected in a triangle, and to the root
    anything else to generate a random graph

The second parameter determines the number of nodes of the random graph.

It is recommended that graphviz be installed, for example using
python3.7 -m pip install graphviz

If it is installed, a pdf of the generated graph will be created

Some example calls:
python3.7 creator.py 2
python3.7 creator.py -1 4