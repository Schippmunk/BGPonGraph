
import random
# system vars
filename = 'bgp.pml'
file_list = []

# program vars

# random graph vars
max_nodes = 6
min_nodes = 4


# the graph
g = None


# File output functions
def create_pml_file() -> None:
    """Saves all the lines of file_list to the file filename"""

    content = "\n".join(file_list)
    with open(filename, 'w+') as the_file:
        the_file.write(content)


def app(lines = '', tabs: int = 0) -> None:
    """lines is a string or an array of strings. This function appends it to the file_list"""
    lines = tab(tabs) + lines
    global file_list
    if isinstance(lines, str):
        file_list.append(lines)
    else:
        file_list = file_list + lines
    
    
def tab(amount: int = 1) -> str:
    return '    ' * amount


class Graph:
    """The graph has the nodes 0...(nodes-1). 0 corresponds to t, 1 to n0, 2 to n1, etc"""
    # number of nodes in the graph, 1 is just t
    nodes = 1
    # adjacency matrix
    ad_mat = []
    # transpose adjacency matrix
    trans_ad_mat = []
    # contract table
    contract_table = []
    # maximum cost generated by t
    max_cost = 8
    # generate a random contract table
    random_contract_table = True

    def get_successors(self, i: int) -> list:
        """Returns list of nodes that are successors of node i"""
        ret = []
        for j in range(self.nodes):
            if self.ad_mat[i][j] == 1:
                ret.append(j)
        return ret
    
    def get_predecessors(self, i: int) -> list:
        """Returns list of nodes that are predecessors of node i"""
        ret = []
        for j in range(self.nodes):
            if self.trans_ad_mat[i][j] == 1:
                ret.append(j)
        return ret

    def get_contract_table(self, i: int, j: int) -> list:
        """Returns the contract table between nodes i and j, if there exists an edge from i to j"""
        if i == 0 and self.exists_edge(j, i): # if i is the target and there exists an edge between j and the target
            targetPred = self.get_predecessors(0) #target's predecessors
            for pos in range(len(targetPred)): # find its position among the target's predecessors
                if j == targetPred[pos]:
                    ret = self.contract_table[i][pos]
        elif i!= 0:
            if self.exists_edge(i, j):
                nodeSucc = self.get_successors(i) #successors of node i
                decreasePos = (0 in nodeSucc) #if the target belongs to the successors of i, there is no contract table for it, so we need to decrease the j's position value
                # find j's position among the successors of i
                for pos in range(len(nodeSucc)):
                    if j == nodeSucc[pos]: # j is the pos-th successor of i
                        if decreasePos:
                            pos -= 1
                        ret = self.contract_table[i][pos]
            else:
                ret = []
        return ret

    def exists_edge(self, i: int, j: int) -> bool:
        """Returns true if there exists an edge from i to j and false otherwise"""
        return self.ad_mat[i][j]

    def generate_random_contract_table(self):
        #target node
        target_contract_table = []
        for pred in self.get_predecessors(0):
            v = random.choice(range(self.max_cost))
            target_contract_table.append(v)
        self.contract_table.append(target_contract_table)
        for node in range(1, self.nodes):
            node_contract_table = []
            for suc in self.get_successors(node):
                if suc != 0:
                    list_of_values = list(range(self.max_cost))
                    random.shuffle(list_of_values)
                    node_contract_table.append(list_of_values)

            self.contract_table.append(node_contract_table) 

    def read_graph_from_file(self):
    	file = open("graph_adjMatrix.txt", "r")
    	contents = file.read()
    	contents = list(contents)
    	adj_matrix_file = []
    	# remove the first and the last braces
    	contents.pop(0)
    	contents.pop()
    	# dummy parsing...
    	for c in contents:
    		if c == '{':
    			row = []
    		elif c == '}':
    			adj_matrix_file.append(row)
    		elif c == ',':
    			pass
    		else:
    			row.append(int(c))
    	self.nodes = len(adj_matrix_file[0])
    	self.ad_mat = adj_matrix_file


    def print_graph(self, transpose: bool = False, view_img: bool = True) -> None:
        """prints the graph pretty"""
        # requires graphviz, install using
        # python3.7 -m pip install graphviz
        from graphviz import Digraph
        dot = Digraph()
        for i in range(self.nodes):
            dot.node(str(i), get_pml_node_name(i))
        edges = []
        for i in range(self.nodes):
            for j in range(self.nodes):
                if transpose:
                    if self.trans_ad_mat[i][j] == 1:
                        edges.append(str(i) + str(j))
                else:
                    if self.ad_mat[i][j] == 1:
                      edges.append(str(i) + str(j))
        dot.edges(edges)
        if transpose:
            dot.render('reverse_graph', view = view_img)
        else:
            dot.render('graph', view = view_img)

    def write_graph_file(self, file_name, transposed: bool = False):
        '''Writes the graph as a linked list into a file'''
        file = open(file_name, "w+")
        file.write("Graph\n")
        for n in range(self.nodes):
            file.write("%d ->" % n)
            if transposed:
                for p in self.get_predecessors(n):
                    file.write(" %d" % p)
            else:
                for s in self.get_successors(n):
                    file.write(" %d" % s)
            file.write("\n")
        file.close()


    def __init__(self, number: int):
        if number == 0+1:
            self.nodes = 1
            self.ad_mat = [[1]]
        elif number == 1+1:
            self.nodes = 2
            self.ad_mat = [[0,0], [1,0]]
        elif number == 2+1:
            # this was the standard model we discussed
            self.nodes = 4
            self.ad_mat = [[0,0,0,0],[1,0,1,0],[1,0,0,1],[1,1,0,0]]
            self.contract_table = [[1, 1, 1], [[0, 0]], [[0, 0]], [[0, 0]]]
            self.max_cost = 2
            self.random_contract_table = False
        elif number == 3+1:
            # another example discussed in the lab
            self.nodes = 3
            self.ad_mat = [[0,0,0],[1,0,1], [1,1,0]]
        elif number == 0:
        	self.read_graph_from_file()
        	#self.read_contract_table_from_file()
        	#self.generate_random_contract_table = False
        else:
            # create a random graph
            self.nodes = random.randrange(min_nodes, max_nodes) #define the number of nodes
            n_edges = random.randrange(self.nodes-1, (self.nodes-1)*(self.nodes-1)) #define the number of edges 
            #print("n_nodes: {}".format(self.nodes))
            #print("n_edges: {}".format(n_edges))

            # empty adjacency matrix
            self.ad_mat = [[0 for x in range(self.nodes)] for x in range(self.nodes)]

            # begin by linking some random node to target
            i = random.randrange(1, self.nodes)
            self.ad_mat[i][0] = 1
            n_edges -= 1 

            # fill the graph with n_edges
            while n_edges != 0:
            	# choose a random source node for the edge
            	i = random.randrange(self.nodes)
            	# there should only be out edges from target, so if i is the target, we should find some other node to be the source of the edge we're adding
            	while i == 0 or sum(self.ad_mat[i]) == (self.nodes-1):
            		i = random.randrange(self.nodes) 
            	# choose a random target node for the edge
            	j = random.randrange(self.nodes)
            	# make sure that i and j are different nodes and that there is no edge from i to j already
            	while i == j or self.exists_edge(i,j): 
            		j = random.randrange(self.nodes)
            	# add the edge between i and j
            	self.ad_mat[i][j] = 1
            	n_edges -= 1

            # # fill the ad_mat
            # for i in range(self.nodes):
            #     for j in range(self.nodes):
            #         if i != j and i != 0:
            #             self.ad_mat[i][j] = random.randrange(2)

                    # else:
                    #     self.ad_mat[i][j] = 0 

        # transposed adjacency matrix
        self.trans_ad_mat = [[0 for x in range(self.nodes)] for x in range(self.nodes)]
        for i in range(self.nodes):
            for j in range(self.nodes):
                self.trans_ad_mat[j][i] = self.ad_mat[i][j]


        if self.random_contract_table:
        	# generate a random contract table with values in Z_max_cost
       		self.generate_random_contract_table()

        self.print_graph(False, True)  # Transposed = False, view = False
        #self.print_graph(True, False)   # Transposed = True, view = False

        self.write_graph_file('generated_graph.txt') 
        self.write_graph_file('generated_graph_transposed.txt', True)
        #self.write_contract_table_file('generated_contract_table.txt')

# helpers
def get_pml_node_index(i: int) -> str:
    if i == 0:
        return '0'
    else:
        return str(i)

def get_pml_node_name(i: int) -> str:
    """Maps node index from our graph representation to pml naming"""
    if i == 0:
        return 't'
    else:
        return 'n' + get_pml_node_index(i)

def get_pml_chan_name(i: int, j: int = 0) -> str:
    """given two node indices, returns the name of the communication channel between them"""
    if i == 0:
        return 't' + get_pml_node_index(j)
    elif j == 0:
        return 't' + get_pml_node_index(i)
    else:
        # maybe this has to be
        # return 'c' + str(j-1) + str(i-1)
        #return 'c' + str(i-1) + str(j-1)
        return 'c' + get_pml_node_name(i) + get_pml_node_name(j) 
        #i'ld say we could name it however we want and this way there won't be any doubts 
        #(note that c111 between nodes 1 and 11 is the same as c111 between nodes 11 and 1 and they should be different channels)
    

# graph to pml
def app_pml() -> None:
    """This function calls all the append to pml functions in correct order"""
    app_constants()
    app()

    app_path()
    app()

    app_channels()
    app()

    app_ltl_spec()
    app()

    app_t_proctype()
    app()

    for i in range(1, g.nodes):
        app_n_proctype(i)
        #app_n_proctype_dummyBGP(i)
        app()
        
def app_constants() -> None:
    app('#define max_cost ' + str(g.max_cost))
    app('#define num_nodes ' + str(g.nodes))

def app_path() -> None:
    app('typedef path {')
    app('byte cost = max_cost;', 1)
    app('byte length = 0;', 1)
    num = g.nodes - 2
    app('byte nodes[' + str(num) + '] = {' + ', '.join([str(g.nodes) for i in range(num)]) + '}', 1)
    app('}')

# add a channel for each edge
def app_channels() -> None:
    for i in range(g.nodes):
        for j in range(g.nodes):
            edge = g.ad_mat[i][j]
            if edge == 1:
                app('chan ' + get_pml_chan_name(j,i) + ' = [1] of {path}')

def app_ltl_spec() -> None:
    """Specifies ltl property that eventually always all channels are empty"""
    prefix = 'ltl converges {eventually always ('
    infix = ''
    for i in range(g.nodes):
        for j in range(g.nodes):
            edge = g.ad_mat[i][j]
            if edge == 1:
                infix = infix + '(len(' + get_pml_chan_name(j,i) + ') == 0) && '
    if infix[-4:] == ' && ':
        infix = infix[:len(infix) - 4]
    suffix = ')}'
    app(prefix + infix + suffix)

def app_t_proctype() -> None:
    app('active proctype t() {')
    for i in g.get_predecessors(0):
        value = g.get_contract_table(0, i)
        path_name = 'p' + get_pml_node_index(i)  
        app('path ' + path_name + ';', 1)
        app(path_name + '.cost = ' + str(value) + ';', 1)
        app(get_pml_chan_name(i) + ' ! ' + path_name + ';', 1)
    app('}')

def app_n_proctype(i: int) -> None:
    # get neighbours
    succ = g.get_successors(i)
    pred = g.get_predecessors(i)

    app('active proctype ' + get_pml_node_name(i) + '() {')
    # x is a variable used for computations
    app('byte x;', 1)
    # p is a variable of type path, also retreived from channels, modified and sent
    app('path p;', 1)
    # list of all paths of outgoing edges
    app('path paths[' + str(len(succ) + 1) + '];', 1)
    # current minimum index
    app('byte cmi = ' + str(len(succ)) + ';', 1)

    # load the contract table between node i and succ[j]
    for j in range(len(succ)):
        if succ[j] != 0:
            table_name = 'cont_' + get_pml_node_name(succ[j])
            contract_table = g.get_contract_table(i,succ[j])
            contract_list = ', '.join(map(str, contract_table))
            app('byte ' + table_name + '[max_cost] = {' + contract_list + '};', 1)

    app()
    # start the loop
    if len(succ) > 0:
        app('do', 1)

    for j in range(len(succ)):
        # recieve value and path from j-th successor
        app('::  ' + get_pml_chan_name(succ[j], i) + ' ? p;', 1)
        # x is the cost the contract prescribes
        if succ[j] == 0:
            app('x = p.cost;', 2)
        else:
            app('x = cont_' + get_pml_node_name(succ[j]) + '[p.cost];', 2)
        app('if', 2)
        app('::  (x < paths[cmi].cost);', 2)
        app('if', 3)
        # check if path is valid
        condition = [get_pml_node_index(i) + ' != p.nodes[' + str(k) + ']' for k in range(g.nodes - 2)]
        condition = ') && ('.join(condition)
        app('::  ((p.length < num_nodes - 2) && (' + condition + '));', 3)
        # update path
        app('cmi = ' + str(j) + ';', 4)
        # this is effectively paths[cmi] = p but promela does not support assignments of whole types
        app('paths[cmi].cost = x;', 4)
        app('paths[cmi].length = p.length + 1;', 4)
        for k in range(g.nodes - 2):
            app('paths[cmi].nodes[' + str(k) + '] = p.nodes[' + str(k) + '];', 4)
        app('paths[cmi].nodes[p.length] = ' + get_pml_node_index(i) + ';', 4)
        app('::  else -> true', 3) # instead of true select previous min path and send it
        app('fi', 3)
        # SEND THE PATH THAT IT USES TO GET THE MINIMUM COST
        app('if', 3)
        app('::  (cmi != ' + str(len(succ)) + ');', 3)
        for k in pred:
            if k != 0:
                app(get_pml_chan_name(i, k) + ' ! paths[cmi]', 4)
        app('::  else -> true', 3)
        app('fi', 3)
        app('::  else -> true', 2)
        app('fi', 2)

    if len(succ) > 0:
        app('od', 1)
    app('}')

# init
def main(arg: list = []) -> None:
    global g
    if len(arg) == 2:
        g = Graph(int(arg[1]))
    else:
        g = Graph(-1)

    app_pml()
    create_pml_file()

if __name__ == "__main__":
    """Run with python3.7 """
    import sys
    main(sys.argv)