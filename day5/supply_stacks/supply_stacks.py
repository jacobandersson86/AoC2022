import argparse
import copy

def readInstructionsFrom(file : str) :
    # Just find the instructions
    with open(file, 'r') as f :
        instructions = []
        for line in f.readlines() :
            words = line.split()

            if len(words) :
                if words[0] == 'move' :
                    instructions.append(words)

    return instructions

def keyToCharacterPosition(key : str) :
    number = int(key)
    return (number - 1) * 4 + 1

def readStackUpFrom(file : str) :
    with open(file, 'r') as f :

        # find number row by stepping line by line
        numberWords = []
        crates = []
        while True :
            line = f.readline()
            words = line.split()

            if len(words) :
                if words[0] == '1' :
                    numberWords = words
                    break
            # If not numbers, add line to list
            crates.append(line)

        # Empty dictionary to initialize the stackUp
        stackUp = {}

        # Read lines backwards and fill up the lists in the dictionary.
        end = int(numberWords[-1])
        for line in reversed(crates) :
            for key in numberWords:
                # if the identifier is longer than the length, skip
                if keyToCharacterPosition(key) > len(line):
                    break
                c = line[keyToCharacterPosition(key)]
                if c.isalpha():
                    # print(f"Adding '{c}' to key {key} from line {line}")
                    try:
                        stackUp[key].append(c)
                    except KeyError :
                        stackUp[key] = []
                        stackUp[key].append(c)

        return stackUp

def executeInstructions(stackUp, instructions) :
    for line in instructions :
        n = int(line[1])
        fromBin = line[3]
        toBin = line[5]
        # print (f"Moving from bin {fromBin} to {toBin} {n} times")
        for n in range(n):
            item = stackUp[fromBin].pop()
            stackUp[toBin].append(item)

    return stackUp

def executeInstructions9001(stackUp, instructions) :
    for line in instructions :
        n = int(line[1])
        fromBin = line[3]
        toBin = line[5]
        # print (f"Moving from bin {fromBin} to {toBin} {n} times")
        item = []
        for n in range(n):
            item.append(stackUp[fromBin].pop())

        item.reverse()
        stackUp[toBin].extend(item)

    return stackUp

def printLastElements(stackUp) :
    solution = ""
    for key in stackUp.keys() :
        solution += stackUp[key][-1]
    print(solution)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", required=True)

    args = parser.parse_args()

    instructions = readInstructionsFrom(args.file)
    stackUp = readStackUpFrom(args.file)
    stackUp2 = copy.deepcopy(stackUp)

    stackUp = executeInstructions(stackUp, instructions)
    stackUp2 = executeInstructions9001(stackUp2, instructions)

    print("Solution 1:")
    printLastElements(stackUp)

    print("Solution 2:")
    printLastElements(stackUp2)
