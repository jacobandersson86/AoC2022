
ROCK = 'X'
PAPER = 'Y'
SCISSOR = 'Z'

ROCK_OPPONENT = 'A'
PAPER_OPPONENT = 'B'
SCISSOR_OPPONENT = 'C'

ROCK_SCORE = 1
PAPER_SCORE = 2
SCISSOR_SCORE = 3

LOST = 0
DRAW = 3
WON = 6

def hand_score(hand : str) -> int:
    if hand == ROCK :
        return ROCK_SCORE
    elif hand == PAPER :
        return PAPER_SCORE
    elif hand == SCISSOR :
        return SCISSOR_SCORE

# Part 1
games = []
with open('./input/input.txt', 'r') as f:
    for line in f.readlines():
        games.extend([str.split(line)])

score = 0
for game in games:
    # Calculate score based on hand
    hand = game[1]
    score += hand_score(hand)

    # Calculate score based on result
    opponent = game[0]

    if opponent == ROCK_OPPONENT :
        if hand == ROCK :
            score += 3
        elif hand == PAPER :
            score += 6
        elif hand == SCISSOR :
            score += 0

    if opponent == PAPER_OPPONENT :
        if hand == ROCK :
            score += 0
        elif hand == PAPER :
            score += 3
        elif hand == SCISSOR :
            score += 6

    if opponent == SCISSOR_OPPONENT :
        if hand == ROCK :
            score += 6
        elif hand == PAPER :
            score += 0
        elif hand == SCISSOR :
            score += 3
# Answer
print(score)

# Part 2
LOSE = 'X'
DRAW = 'Y'
WIN = 'Z'

score = 0
for game in games:
    opponent = game[0]
    result = game[1]

    if result == DRAW :
        score += 3
    if result == WIN :
        score += 6

    if opponent == ROCK_OPPONENT :
        if result == DRAW :
            hand = ROCK
        elif result == WIN :
            hand = PAPER
        elif result == LOSE :
            hand = SCISSOR

    elif opponent == PAPER_OPPONENT :
        if result == DRAW :
            hand = PAPER
        elif result == WIN :
            hand = SCISSOR
        elif result == LOSE :
            hand = ROCK

    elif opponent == SCISSOR_OPPONENT :
        if result == DRAW :
            hand = SCISSOR
        elif result == WIN :
            hand = ROCK
        elif result == LOSE :
            hand = PAPER

    score += hand_score(hand)

print(score)
