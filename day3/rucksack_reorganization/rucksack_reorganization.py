import argparse
from itertools import chain

def contentOf(file) :
    rucksacks = []
    with open(args.file, 'r') as f:
        for line in f.readlines():
            line = line.replace("\n","")
            content = list(line) # List constructor split to characters
            rucksacks.append(content)
    return rucksacks

def split(rucksack : list) -> tuple :
    # Always same amount of items in each compartment
    numberOfItems = len(rucksack)
    if numberOfItems % 2 != 0 :
        raise Exception("Odd number of items")
    middle = int(numberOfItems/2)
    return rucksack[:middle], rucksack[middle:]

def commonItems(first : list, second : list) :
    common = list (set(first) & set(second))
    return common

def commonItem3(first : list, second : list, third : list) :
    common1 = commonItems(first, second)
    common2 = commonItems(second, third)
    common = commonItems(common1, common2)
    return common

def partOne(rucksacks, priority) :
    score = 0
    for rucksack in rucksacks :
        first, second = split(rucksack)
        items = commonItems(first, second)
        score += priority[items[0]]

    print(f"Solution 1: {score}")

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def partTwo(rucksacks, priority) :
    score = 0
    groups = list(chunks(rucksacks, 3))
    print (f"Number of groups: {len(list(groups))}, rucksacks: {len(rucksacks)}")
    for rucksacks in groups :
        items = commonItem3(rucksacks[0], rucksacks[1], rucksacks[2])
        score += priority[items[0]]

    print(f"Solution 2: {score}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", required=True)

    args = parser.parse_args()

    # Create a dictionary for the priority
    keys1 = (chr(n) for n in range(ord('a'), ord('z') + 1))
    keys2 = (chr(n) for n in range(ord('A'), ord('Z') + 1))
    keys = chain(keys1, keys2)
    values = range(1, 52 + 1)
    priority = dict(zip(keys, values))

    # Check the contents
    score = 0
    rucksacks = contentOf(args.file)

    partOne(rucksacks, priority)
    partTwo(rucksacks, priority)
