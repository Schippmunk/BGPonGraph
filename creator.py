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
    # number of nodes in the graph, 1 is just t
    nodes = 1
    # adjacency matrix
    ad_mat = [[0]]

    def print():
    # prints the graph pretty
        pass

    def __init__(self, number: int) -> Graph:
        """Creates example Graph"""
        if number == 0:
            self.nodes = 1
            self.ad_mat = [[1]]
        elif number == 1:
            self.nodes = 2
            self.ad_mat = [[0,1], [1,0]]

    def __init__(self) -> Graph:
        """Creates a random Graph"""
        pass

# graph to pml
def app_pml() -> None:
    app_channels()

def app_channels() -> None:
    pass
    #app("chan t" + str(i) + " = [1] of {byte}")


def main(arg: list = []) -> None:
    global g
    if len(arg) == 2
        g = Graph(int(arg[1]))
    else:
        g = Graph()

    app_pml()
    create_pml_file()

if __name__ == "__main__":
    import sys
    main(sys.argv)
