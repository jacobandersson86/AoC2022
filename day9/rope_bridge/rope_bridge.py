import argparse
import math

# Initial state of head and tail.
class Rope :

    def __init__ (self) :
        self.head = {}
        self.tail = {}
        self.tail_positions = []
        self.setHead(0,0)
        self.setTail(0,0)

    def _addPosition(self, x, y) :
        self.tail_positions.append([x, y])

    def setHead(self, x, y) :
        self.head['x'] = x
        self.head['y'] = y

    def setTail(self, x, y) :
        self.tail['x'] = x
        self.tail['y'] = y
        self._addPosition(x, y)

    def getHead(self):
        return self.head.get('x'), self.head.get('y')

    def getTail(self):
        return self.tail.get('x'), self.tail.get('y')

    def updateTail(self) :
        ds, dx, dy = distance(self.head['x'], self.head['y'], self.tail['x'], self.tail['y'])
        if ds < 2 :
            return

        x, y = self.getHead()
        if dx == 2 :
            x += 1
        elif dx == -2 :
            x -= 1
        if dy == 2 :
            y += 1
        elif dy == -2 :
            y -= 1
        # else :
        #     print("error")
        self.setTail(x, y)

    def executeMove(self, move):
        match move[0]:
            case 'U' :
                self.head['y'] += 1
            case 'D' :
                self.head['y'] -= 1
            case 'R' :
                self.head['x'] += 1
            case 'L' :
                self.head['x'] -= 1


def readFile(file) :
    with open(file, 'r') as f :
        moves = []
        for line in f.readlines() :
            line = line.strip().split()
            moves.append(line)
    return moves

def distance(x0, y0, x1, y1) :
    dx = x1 - x0
    dy = y1 - y0
    return math.sqrt(dx**2 + dy**2), dx, dy

def executeMovement(move, ropes : [Rope]) :
    for _ in range(0,int(move[1])) :
        # Move the first ropes head
        ropes[0].executeMove(move)

        # Update tail, the ropes tail as
        # the next ropes head.
        for i, _ in enumerate(ropes[ : -1]):
            ropes[i].updateTail()
            x, y = ropes[i].getTail()
            # print (f"tail({i}): ({x}, {y})")
            ropes[i+1].setHead(x, y)

        # Finally update last tail
        ropes[-1].updateTail()

# def findUniquePositions(positions) :
#     hashed_positions = []
#     for coordinate in positions:
#         val = hash((coordinate[0], coordinate[1]))
#         hashed_positions.append(val)
#     return set(hashed_positions)

def findUniquePositions(positions) :
    str_positions = []
    for coordinate in positions:
        str_positions.append(str(coordinate[0])+str(coordinate[1]))
    return set(str_positions)

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", required=True)
    parser.add_argument("--ropes", "-r", required=True)

    args = parser.parse_args()

    moves = readFile(args.file)

    ropes = [Rope() for _ in range(int(args.ropes))]
    for move in moves :
        executeMovement(move, ropes)

    # print(ropes[-1].tail_positions)
    print(len(ropes[-1].tail_positions))
    unique = findUniquePositions(ropes[-1].tail_positions)
    print(f"Solution : {len(unique)}")
