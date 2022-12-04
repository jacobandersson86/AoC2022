import argparse

def contentOf(file):
    with open(args.file, 'r') as f:
        for line in f.readlines():
            line = line.replace("\n","").split(',')
            yield line

def parseScheduleToGenerator(pair) :
    for schedule in pair:
        limits = schedule.split('-')
        yield list(range(int(limits[0]), int(limits[1]) + 1))

def createSets(duties) :
    dutySets = []
    for pair in duties :
        thisPair = list(parseScheduleToGenerator(pair))
        dutySets.append(thisPair)
    return dutySets

def compareSetsFullyContains(dutySets) :
    score = 0
    for duty in dutySets:
        a = set(duty[0])
        b = set(duty[1])
        isContained = b.issubset(a) or b.issuperset(a)
        score += 1 if isContained else 0

    return score

def compareSetsIntersect(dutySets) :
    score = 0
    for duty in dutySets:
        a = set(duty[0])
        b = set(duty[1])
        c = a.intersection(b)
        score += 1 if c else 0

    return score

def partOne(dutySets) :
    score = compareSetsFullyContains(dutySets)

    print(f"Solution 1 : {score}")

def partTwo(dutySets) :
    score = compareSetsIntersect(dutySets)

    print(f"Solution 2 : {score}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", required=True)

    args = parser.parse_args()

    duties = list(contentOf(args.file))
    dutySets = createSets(duties)

    partOne(dutySets)
    partTwo(dutySets)
