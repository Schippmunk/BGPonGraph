
# system vars
filename = 'bgp.pml'
file_list = []

# program vars

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


class Graph:
    """The graph has the nodes 0...(nodes-1). 0 corresponds to t, 1 to n0, 2 to n1, etc"""
    # number of nodes in the graph, 1 is just t
    nodes = 1
    # adjacency matrix
    ad_mat = []

    def print_graph(self):
        """prints the graph pretty"""
        # requires graphviz, install using
        # python3.7 -m pip install graphviz
        from graphviz import Digraph
        dot = Digraph()
        for i in range(self.nodes):
            dot.node(str(i), str(i))
        edges = []
        for i in range(self.nodes):
            for j in range(self.nodes):
                if self.ad_mat[i][j] == 1:
                    edges.append(str(i) + str(j))
        dot.edges(edges)
        #print(dot.source)
        dot.render('graph', view = True)

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
            """Creates a random Graph"""
            import random
            self.nodes = random.randrange(1,6)
            for i in range(0,self.nodes):
                row = []
                for j in range(0,self.nodes):
                    row.append(random.randrange(2))
                self.ad_mat.append(row)

        self.print_graph()

# graph to pml
def app_pml() -> None:
    app_channels()
    app('')
    app_t_proctype()
    app('')
    for i in range(0, g.nodes - 1):
        app_n_proctype(i)
        app('')

def app_channels() -> None:
    for i in range(g.nodes):
        for j in range(g.nodes):
            edge = g.ad_mat[i][j]
            if edge == 1:
                if i != 0 and j == 0:
                    # channel from ni to t
                    app('chan t' + str(i-1) + ' = [1] of {byte}')
                elif i != 0 and j != 0 and i != j:
                    # channel cij
                    app('chan c' + str(i-1) + str(j-1) + ' = 1 of {byte}')

def app_t_proctype() -> None:
    app('active proctype t() {')
    #
    #
    app('}')

def app_n_proctype(number: int) -> None:
    app('active proctype n' + str(number) + '() {')
    #
    #
    app('}')



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
