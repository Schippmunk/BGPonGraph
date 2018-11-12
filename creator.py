# system vars
filename = 'bgp.pml'
file_list = []

# program vars
n = 256
# nodes are 0 to 3, 0 is target
nodes = 4
edges = ()

def save_file():
    content = "\n".join(file_list)
    with open(filename, 'w+') as the_file:
        the_file.write(content)


def app(lines):
    global file_list
    if isinstance(lines, str):
        file_list.append(lines)
    else:
        file_list = file_list + lines

def preprocessor():
    """Adds preprocessor cmds like define to the beginning of the list"""
    app('#define n ' + str(n))


def create_edges():
    global edges
    for i in range(nodes):
        edges.append([i+1, i])


def main():
    create_edges()
    preprocessor()
    savefile()

if __name__ == "__main__":
    main()
