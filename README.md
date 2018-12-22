# BGPonGraph

This is a python program that creates a Promela file simulating the Boarder Gateway Protocol Algorithm on a graph.

How to run:
python3.7 creator.py [example_number] [number_nodes]

example_number can be:
    0 to read a graph from a file. 
	The enclosing folder must contain a file named “graph.txt”
	with a directed graph given by its adjacency matrix 
	written as a list of lists with curly braces 
	(e.g. {{1, 0}, {0, 1}} would be the identity matrix of dimension 2). 
	The first node represents the root(or target). 
	The enclosing folder must contain a file named “contract_table.txt” 
	with the graph’s corresponding contract table given as a list of lists with curly braces.
	The first one is a list of the costs of using the root (or target) channels.
	The others are lists of lists. Each one corresponds to the contracts between the node and its neighbours.
	Hence, each node’s list has as many lists as the node outdegree (-1 if it is connected to the root),
	each of them with the contract between the node and its neighbour.
	(e.g. in Z2: {{1,1}, {{0,1},{0,1}},{},{{0,1}}} corresponds to the contract table of a graph with 4 nodes, 
	2 of them linked to the root, whose channels have a cost of 1. The node1 (considering the root as node0)
	has outdegree 2 and the contract table between the node and its neighbours is the identity, 
	node2 has no outgoing edges besides the one linking to target, 
	node3 has an outgoing edge to some other node and the contract table between them is also the identity.

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
