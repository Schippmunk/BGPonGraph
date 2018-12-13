
import random
# system vars
filename = 'bgp.pml'
file_list = []

# program vars

# random graph vars
max_nodes = 6
min_nodes = 5

# the graph
g = None


# File output functions
def create_pml_file() -> None:
    """Saves all the lines of file_list to the file filename"""

    content = "\n".join(file_list)
    with open(filename, 'w+') as the_file:
        the_file.write(content)


def app(lines) -> None:
    """lines is a string or an array of strings. This function appends it to the file_list"""
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
    max_cost = 255

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

    def get_contractTable(self, i: int, j: int) -> list:
        """Returns the contract table between nodes i and j, if there exists an edge from i to j"""
        if self.existsEdge(i,j):
            ret = contractTable[i, j]
        else:
            ret = []
        return ret

    def existsEdge(self, i: int, j: int) -> bool:
        """Returns true if there exists an edge from i to j and false otherwise"""
        return self.ad_mat[i][j]

    def generate_random_contract_table(self):
        for node in range(self.nodes):
            nodeContractTable = []
            for suc in self.get_successors(node):
                listOfValues = list(range(self.max_cost)) #assuming the costs are in Z8 for now....
                random.shuffle(listOfValues)
                nodeContractTable.append(listOfValues)
            self.contract_table.append(nodeContractTable) 


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

    def __init__(self, number: int):
        if number == 0:
            self.nodes = 1
            self.ad_mat = [[1]]
        elif number == 1:
            self.nodes = 2
            self.ad_mat = [[0,0], [1,0]]
        elif number == 2:
            # this was the standard model we discussed
            self.nodes = 4
            self.ad_mat = [[0,0,0,0],[1,0,1,0],[1,0,0,1],[1,1,0,0]]
        elif number == 3:
            # another example discussed in the lab
            self.nodes = 3
            self.ad_mat = [[0,0,0],[1,0,1], [1,1,0]]
        else:
            # create a random graph
            self.nodes = random.randrange(min_nodes, max_nodes)

            # empty adjacency matrix
            self.ad_mat = [[0 for x in range(self.nodes)] for x in range(self.nodes)]
            
            # fill the ad_mat
            for i in range(self.nodes):
                for j in range(self.nodes):
                    if i != j and i != 0:
                        self.ad_mat[i][j] = random.randrange(2)
                    else:
                        self.ad_mat[i][j] = 0

        # transposed adjacency matrix
        self.trans_ad_mat = [[0 for x in range(self.nodes)] for x in range(self.nodes)]
        for i in range(self.nodes):
            for j in range(self.nodes):
                self.trans_ad_mat[j][i] = self.ad_mat[i][j]

        # generate a random contract table with values in Z8 (for now...)
        self.generate_random_contract_table()

        self.print_graph(False, False)
        self.print_graph(True, False)

# helpers
def get_pml_node_name(i: int) -> str:
    """Maps node index from our graph representation to pml naming"""
    if i == 0:
        return 't'
    else:
        return 'n' + str(i-1)

def get_pml_chan_name(i: int, j: int = 0) -> str:
    """given two node indices, returns the name of the communication channel between them"""
    if i == 0:
        return 't' + str(j-1)
    elif j == 0:
        return 't' + str(i-1)
    else:
        # maybe this has to be
        # return 'c' + str(j-1) + str(i-1)
        return 'c' + str(i-1) + str(j-1)
        # return 'c' + get_pml_node_name(i) + get_pml_node_name(j) 
        #i'ld say we could name it however we want and this way there won't be any doubts 
        #(note that c111 between nodes 1 and 11 is the same as c111 between nodes 11 and 1 and they should be different channels)
    

# graph to pml
def app_pml() -> None:
    """This function calls all the append to pml functions in correct order"""
    app_constants()
    app('')

    app_channels()
    app('')

    app_ltl_spec()
    app('')

    app_t_proctype()
    app('')

    for i in range(1, g.nodes):
        #app_n_proctype(i)
        app_n_proctype_dummyBGP(i)
        app('')
        
def app_constants() -> None:
    app('#define max_cost ' + str(g.max_cost))

# add a channel for each edge
def app_channels() -> None:
    for i in range(g.nodes):
        for j in range(g.nodes):
            edge = g.ad_mat[i][j]
            if edge == 1:
                app('chan ' + get_pml_chan_name(j,i) + ' = [1] of {byte}')

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
        app(tab() + get_pml_chan_name(i) + '!' + str(random.randrange(1, g.max_cost + 1)) + ';') #why some random number?
    app('}')

def app_n_proctype_dummyBGP(i: int) -> None:
    app('active proctype ' + get_pml_node_name(i) + '() {')
    var_e = 'e' + str(i-1)
    app(tab() + 'byte ' + var_e + ' = max_cost;')
    app(tab() + 'byte x = 0;')
    succ = g.get_successors(i)
    pred = g.get_predecessors(i)
    # I think this could be done like this: (which means setting each value of v[] as max_cost)
    #app(tab() + 'byte v[' + str(len(succ)) + '] = max_cost;') 
    app(tab() + 'byte v[' + str(len(succ)) + '];')
    for j in range(len(succ)):
        app(tab() + 'v[' + str(j) + '] = max_cost;')
    app('')

    app(tab() + 'do')
    for j in range(len(succ)):
        app(tab(2) + ':: ' + get_pml_chan_name(i,succ[j]) + '?x;')
        if succ[j] != 0:
            app(tab(3) + 'if')
            app(tab(4) + ':: x > 0 -> x = x - 1')
            app(tab(3) + 'fi;')
        app(tab(3) + 'if')
        array_element = 'v[' + str(j) + ']'
        app(tab(4) + ':: x < ' + array_element + ' -> ' + array_element + ' = ' + var_e + ';')
        app(tab(5) + 'if')
        app(tab(6) + ':: x < ' + var_e + ' -> ' + var_e + ' = x;')
        for k in pred:
            if k != 0: # if k is not the target
                app(tab(7) + get_pml_chan_name(i,k) + '!' + var_e + ';') # advertises its minimum cost
        app(tab(5) + 'fi')
        app(tab(3) + 'fi')
    app(tab() + 'od')
    app('}')



def app_n_proctype(i: int) -> None:
    app('active proctype ' + get_pml_node_name(i) + '() {')
    var_e = 'e' + str(i-1)
    app(tab() + 'byte ' + var_e + ' = max_cost;')
    app(tab() + 'byte x = 0;')
    succ = g.get_successors(i) # list of successors
    pred = g.get_predecessors(i) # list of predecessors
    
    #I'm not sure this should be initialized as max_cost...
    # I think this could be done like this (which means setting each value of cost[] as max_cost):
    #app(tab() + 'byte cost[' + str(len(succ)) + '] = max_cost;') 

    app(tab() + 'byte cost[' + str(len(succ)) + '];')
    for j in range(len(succ)):
        app(tab() + 'cost[' + str(j) + '] = max_cost;')
    app('')

    app(tab() + 'do')
    for j in range(len(succ)):
        array_element = 'cost[' + str(j) + ']'
        app(tab(2) + ':: ' + get_pml_chan_name(i,succ[j]) + '?x;') # sets x as the message written from the channel between i and its j-successor
        #app(tab(2) + 'if')        
        #app(tab(3) + ':: ' + array_element + ' > x -> ') 
        if succ[j] != 0:
            # load the contract table between node i and succ[j]
            contractTable = g.get_contract_table(i,succ[j])
            contractValues = 'byte conTableN' + str(i-1) + 'N' + str(succ[j]-1)
            app(tab(2) + contractValues + '[' + str(len(contractTable)) +'];')
            for k in range(len(contractTable)):
                app(tab(2) + contractValues + '[' + str(k) + '] = ' + str(contractTable[k]))
            
            #I'm not sure about this...
            app(tab(3) + 'if')
            app(tab(4) + ':: ' + contractValues +'[x] < cost[' + str(succ[j]-1) + '];')
            app(tab(4) + 'if')
            app(tab(5) + 'path is valid -> cost[' + str(succ[j]-1) + '] = ' + contractValues +'[x]') 
            app(tab(4) + 'fi')
            app(tab(3) + 'fi')
        app(tab(3) + 'if')
        array_element = 'v[' + str(j) + ']'
        app(tab(4) + ':: x < ' + array_element + ' -> ' + array_element + ' = ' + var_e + ';')
        app(tab(5) + 'if')
        app(tab(6) + ':: x < ' + var_e + ' -> ' + var_e + ' = x;')
        for k in pred:
            if k != 0: # if k is not the target
                app(tab(7) + get_pml_chan_name(i,k) + '!' + var_e + ';') # advertises its minimum cost
        app(tab(5) + 'fi')
        app(tab(3) + 'fi')
    app(tab() + 'od')
    app('}')




# given the list name, append a procedure to return the minimum value of that list
# this operation should probably be done atomically... but I'm not sure
def app_get_minimum_proc(chanName, list: str) -> None:
    minValue = 'min' + chanName
    iterator = 'i' + chanName
    app(tab() + 'byte ' + minValue +' = max_cost;')
    app(tab() + 'int ' + iterator + ';')
    app(tab() + 'for('+ iterator + ' in ' + list + '){')
    app(tab(2) + 'if')
    app(tab(3) + ':: ' + minValue + ' >= ' + list + '[' + iterator +'] -> ' + minValue + ' = ' + list + '[' + iterator + '];')
    app(tab(2) + 'fi')
    app(tab() + '}')



# init
def main(arg: list = []) -> None:
    global g
    print(arg)
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