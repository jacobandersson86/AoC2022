import argparse
import numpy as np
import copy
import operator
import random

CLR_CYAN = "\x1b[96m"
CLR_RED = "\x1b[91m"
CLR_GREEN = "\x1b[92m"
CLR_MAGENTA = "\x1b[95m"
CLR_YELLOW = "\x1b[93m"
CLR_BLUE = "\x1b[94m"
CLR_OFF = "\x1b[0m"

class Path :
    # Class globals
    directions = ["up", "down", "left", "right"]
    allVisitedSet = set()
    allPaths = []

    def __init__(self, start, end, map, searchForA = False) :
        self.start = start
        self.head = start
        self.end = end
        self.map = map
        self.visited = [self.start]
        startSet = set([str(self.start)])
        self.visitedSet = startSet
        self.allVisitedSet.update(startSet)
        self.active = True
        self.allPaths.append(self)
        self.searchForA = searchForA
        self.foundA = False

    def _testMove(self, direction) :
        y, x = self.head
        match direction :
            case 'up' :
                y += 1
            case 'down' :
                y -= 1
            case 'right' :
                x += 1
            case 'left' :
                x -= 1

        # Check if outside of map.
        y_len, x_len = self.map.shape
        if x < 0 or y < 0 :
            return False, y, x
        elif x == x_len or y == y_len :
            return False, y, x

        # Check if position has been visited
        # (This part is most likely not very efficient)
        visited_positions = self.allVisitedSet
        thisPosition = set([str((y, x))])
        intersect = visited_positions.intersection(thisPosition)
        if len(intersect) :
            return False, y, x

        # Check if the height is correct
        hy, hx = self.head
        thisHeight = self.map[hy][hx]
        nextHeight = self.map[y][x]

        if not self.searchForA :
            # Can walk one elevation up, but infinite down
            if nextHeight - thisHeight > 1 :
                return False, y, x
        else : # Searching for first a
            # Search from top down, so we can take max one down (-1) but infinite up
            if nextHeight - thisHeight < -1 :
                return False, y, x

        return True, y, x

    def _findPossibleMoves(self) :
        # Check direction
        moves = []
        random.shuffle(self.directions)
        for direction in self.directions:
            possible, y, x = self._testMove(direction)
            if possible :
                moves.append((y, x))
        return moves

    def _makeMove(self, move) :
        # Update the set of visited positions
        self.head = move
        self.visited.append(move)
        thisMoveSet = set([str(move)])
        self.visitedSet.update(thisMoveSet)
        self.allVisitedSet.update(thisMoveSet)
        if self.head == self.end:
            self.active = False
        # Part 2, find first a from top
        if self.searchForA :
            y, x = self.head
            if self.map[y][x] == ord('a') :
                self.foundA = True
                self.active = False

    def search(self) :
        if self.active == False :
            return

        # Check options
        moves = self._findPossibleMoves()

        # No options, this path has reach a dead end
        if len(moves) == 0 :
            # print(f"Path reached dead-end")
            self.active = False

        # If many possibilities, make a copy of the path
        newPaths = [self]
        for _ in range(len(moves) - 1) :
            newPaths.append(copy.deepcopy(self))
            # print(f"New path created. Totally {len(self.allPaths) + len(moves) - 1}")

        # Move a step in each direction
        # Add to the global list of paths
        for i, move in enumerate(moves):
            newPaths[i]._makeMove(move)

            if newPaths[i] == self :
                continue
            self.allPaths.append(newPaths[i])

def readFileToGrid(file : str) :
    grid = []
    with open (file, 'r') as f :
        for line in f.readlines() :
            row = list(line.strip())
            row = [ord(c) for c in row]
            grid.append(row)

    return np.array(grid)

def findStartAndStop(heightMap : np.ndarray) :
    y_len, x_len = heightMap.shape

    for x in range(x_len) :
        for y in range(y_len) :
            if heightMap[y][x] == ord('S') :
                start = (y, x)
                heightMap[y][x] = ord('a') - 1
            if heightMap[y][x] == ord('E') :
                end = (y, x)
                heightMap[y][x] = ord('z') + 1
    return heightMap, start, end

def plotPositions(heightMap, visitedPositions, start, end) :
    visitedMap = np.zeros(heightMap.shape)
    for i, pos in enumerate(visitedPositions) :
        y, x = pos
        visitedMap[y][x] = i + 1

    height, width = heightMap.shape
    output = ""
    sy, sx = start
    ey, ex = end
    for y in range(height):
        for x in range(width) :
            if sy == y and sx == x :
                dot = CLR_GREEN + "S" + CLR_OFF
            elif ey == y and ex == x :
                dot = CLR_RED + "E" + CLR_OFF
            else :
                letter = chr(heightMap[y][x])
                dot = CLR_YELLOW + chr(heightMap[y][x] - 0x20) + CLR_OFF if visitedMap[y][x] else letter
            output += dot
        output += "\n"
    print(output)

def searchTop(heightMap, start, end) :
    # Search path to top
    path = Path(start, end, heightMap)

    # Search maximum 500 deep
    for _ in range(500) :
        # This is to ensure max one step per iteration as .search() will spawn new objects
        nPaths = len(Path.allPaths)
        for i in range(nPaths) :
            Path.allPaths[i].search()

    endSet = set([str(end)])
    lengths = []
    for i, path in enumerate(Path.allPaths) :
        if path.visitedSet.intersection(endSet):
            length = len(path.visited) - 1
            lengths.append((length, i))


    shortest = min(lengths, key=operator.itemgetter(0))
    length, i = shortest


    print(f"Shortest way down (to an 'a') is {length} steps")
    print(f"Found in path no {i}")
    plotPositions(heightMap, Path.allPaths[i].visited, start, end)

def searchForA(heightMap, start, end) :
    # Search path from end to first 'a' (reverse start/end)
    path = Path(end, start, heightMap, searchForA=True)

    # Search maximum 500 deep
    for _ in range(500) :
        # This is to ensure max one step per iteration as .search() will spawn new objects
        nPaths = len(Path.allPaths)
        for i in range(nPaths) :
            Path.allPaths[i].search()

    endSet = set([str(end)])
    lengths = []
    for i, path in enumerate(Path.allPaths) :
        if path.foundA :
            length = len(path.visited) - 1
            lengths.append((length, i))

    shortest = min(lengths, key=operator.itemgetter(0))
    length, i = shortest


    print(f"Shortest way up is {length} steps")
    print(f"Found in path no {i}")
    plotPositions(heightMap, Path.allPaths[i].visited, start, end)

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", required=True)
    parser.add_argument("-s", required = True)

    args = parser.parse_args()
    heightMap = readFileToGrid(args.file)

    heightMap, start, end = findStartAndStop(heightMap)

    if args.s == "1" :
        searchTop(heightMap, start, end)
    elif args.s == "2" :
        searchForA(heightMap, start, end)
