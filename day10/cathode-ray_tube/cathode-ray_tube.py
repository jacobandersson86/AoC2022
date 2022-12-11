import argparse

class Computer:
    def __init__(self) :
        self.cycles = 0
        self.regX = 1
        self.nextValue = 0
        self.snapshots = []

def addX(value, cp) :
    noop(cp)
    cp.nextValue = value
    cp.cycles += 1
    takeSnapshot(cp)

def noop(cp):
    cp.cycles += 1
    takeSnapshot(cp)


def takeSnapshot(cp):
    cp.snapshots.append([cp.cycles, cp.regX])

def executeInstruction(instruction, cp) :
    match instruction[0]:
        case 'addx':
            addX(int(instruction[1]), cp)
        case 'noop':
            noop(cp)

    cp.regX += cp.nextValue
    cp.nextValue = 0

def readFile(file):
    instructions = []
    with open(file, 'r') as f:
        for line in f.readlines():
            instruction = line.strip().split()
            instructions.append(instruction)
    return instructions

def findValueAt(cycle, snapshots : []) :
    for i, snap in enumerate(snapshots):
        if snap[0] > cycle :
            return snapshots[i - 1][1]


def extractSignals(snapshots):
    signals = []
    values = [20, 60, 100, 140, 180, 220]

    for cycle in values:
        signals.append(cycle*findValueAt(cycle, snapshots))

    return signals

def shouldSetPixel(position, regX) :
    horPos = position % 40

    ds = horPos - regX
    if ds >= -1 and ds <= 1 :
        return True
    return False

def renderImage(snapshots):
    output = ""
    for snap in snapshots :
        cycle = snap[0]
        regX = snap[1]

        if shouldSetPixel(cycle - 1, regX) :
            output += '#'
        else :
            output += ' '

        if cycle % 40 == 0 :
            output += '\n'
    return output

if __name__ == "__main__" :

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", required=True)

    args = parser.parse_args()

    instructions = readFile(args.file)

    cp = Computer()
    cp.cycles = 0

    for instruction in instructions :
        executeInstruction(instruction, cp)

    signals = extractSignals(cp.snapshots)
    print(f"Solution 1: {sum(signals)}")

    output = renderImage(cp.snapshots)
    print("Solution 2:\n" + output)
