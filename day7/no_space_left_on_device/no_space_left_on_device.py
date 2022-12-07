import argparse

def removeLastDir(pwd) :
    for i, c in enumerate(reversed(pwd)) :
        newPath = ''
        if c == '/' :
            newPath = pwd[:-(i+1)]
            break
    # if at root, add slash
    if newPath == '' :
        newPath = '/'
    pwd = newPath
    return pwd

def executeCommand(cmd : str, args : list[str], pwd) :
    match cmd :
        case 'cd' :
            if args[0] == '..' :
                pwd = removeLastDir(pwd)
            elif args[0] == '/' :
                pwd = '/'
            else :
                if len(pwd) :
                    if pwd[-1] != '/' :
                        pwd += '/'
                pwd += args[0]
    return pwd

def addSizeToDir(dirSizes, pwd, size) :
    try :
        dirSizes[pwd] += size
    except KeyError :
        dirSizes[pwd] = 0
        dirSizes[pwd] += size
    return dirSizes

def addSizeToSubDirs(dirSizes, pwd, size) :
    while True :
        pwd = removeLastDir(pwd)
        addSizeToDir(dirSizes, pwd, size)
        if pwd == '/' :
            break
    return dirSizes

def eavesdropOnSystem(file : str) -> None:
    pwd = ''
    dirSizes = {}
    with open(file, 'r') as f :
        pwd = ''
        for line in f.readlines() :
            words = line.strip().split(' ')
            if words[0] == '$' :
                cmd = words[1]
                args = words[2:]
                pwd = executeCommand(cmd, args, pwd)
            elif words[0].isnumeric() :
                if pwd != '/':
                    dirSizes = addSizeToDir(dirSizes, pwd, int(words[0]))
                dirSizes = addSizeToSubDirs(dirSizes, pwd, int(words[0]))

    return dirSizes

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", required=True)

    args = parser.parse_args()

    dirSizes = eavesdropOnSystem(args.file)

    solution1 = 0
    for key, size in dirSizes.items():
        if size <= 100000 :
            solution1 += size
    print(f"Solution 1 : {solution1}")

    # Calculate what's needed
    total = 70000000
    unused = total - dirSizes['/']
    needed = 30000000 - unused

    sizes = []
    for dir, size in dirSizes.items():
        if size >= needed :
            sizes.append(size)

    print(f"Solution 2 : {min(sizes)}")
