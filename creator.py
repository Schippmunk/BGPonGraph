

filename = 'bgp.pml'
file_list = []


def savefile():
    content = "\n".join(file_list)
    with open(filename, 'w+') as the_file:
        the_file.write(content)


def app(lines):
    global file_list
    if isinstance(lines, str):
        file_list.append(lines)
    else:
        file_list = file_list + lines


def main():
    app('abc')
    app(['d', 'e' ,'f'])
    savefile()

if __name__ == "__main__":
    main()
