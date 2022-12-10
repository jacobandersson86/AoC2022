import argparse

def isVisibleTree(x, y, grid) :
    y_len = len(grid)
    x_len = len(grid[0])

    # if at edge return false
    if x == 0 or y == 0 :
        return True
    if x == x_len - 1 or y == y_len - 1 :
        return True

    thisHeight = grid[y][x]

    # Check trees to the right
    right = grid[y][:x]
    if max(right) < thisHeight :
        return True

    left = grid[y][(x + 1):]
    if max(left) < thisHeight :
        return True

    up = [grid[idy][x] for idy in reversed(range(0, y))]
    if max(up) < thisHeight :
        return True

    down = [grid[idy][x] for idy in range(y + 1, y_len)]
    if max(down) < thisHeight :
        return True

def calculateScenicScore(x, y, grid) :
    y_len = len(grid)
    x_len = len(grid[0])
    thisHeight = grid[y][x]

    score = 0
    # Iterate from x,y to right edge
    if x > 0 :
        this = 0
        for idx in reversed(range(0, x)) :
            this += 1
            if grid[y][idx] >= thisHeight:
                break
        print(f"x right: {this}")
        score += this

    # Iterate from x,y to left edge :
    if x < x_len - 1 :
        this = 0
        for idx in range(x + 1, x_len) :
            this += 1
            if grid[y][idx] >= thisHeight :
                break
        print(f"x left: {this}")
        score *= this

    if y > 0 :
        this = 0
        for idy in reversed(range(0, y)) :
            this += 1
            print(f"I see {grid[idy][x]} upwards")
            if grid[idy][x] >= thisHeight :
                break
        print(f"y up: {this}")
        score *= this

    if y < y_len - 1 :
        this = 0
        for idy in range(y + 1, y_len) :
            this += 1
            if grid[idy][x] >= thisHeight :
                break
        print(f"y down: {this}")
        score *= this

    return score

def readFileToGrid(file : str) :
    grid = []
    with open (file, 'r') as f :
        for line in f.readlines() :
            row = list(line.strip())
            row = [int(c) for c in row]
            grid.append(row)

    return grid

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", required=True)

    args = parser.parse_args()

    # Make treetop heights accessible as grid[y][x]
    grid = readFileToGrid(args.file)

    score = 0
    scenicScores = []
    for y, row in enumerate(grid) :
        for x, _ in enumerate(row) :
            score += 1 if isVisibleTree(x,y, grid) else 0
            scenicScores.append(calculateScenicScore(x, y, grid))

    print(score)
    print(max(scenicScores))

