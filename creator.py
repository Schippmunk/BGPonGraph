# system vars
filename = 'bgp.pml'
file_list = []

# program vars
n = 256
# nodes are 0 to 3, 0 is target
nodes = 4
edges = ()

def save_file() -> None:
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

def preprocessor() -> None:
    """Adds preprocessor cmds like define to the beginning of the list"""

    app('#define n ' + str(n))

def create_channels() -> None:
    for i in range(0..nodes):
        app("chan t" + str(i) + " = [1] of {byte}")

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
