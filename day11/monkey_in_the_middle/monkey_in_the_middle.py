import argparse

class Monkey :
    def __init__(self, items : [int], operation, test : int) :
        self.items = items
        self.operation = operation
        self.test = test
        self.inspected = 0

    def setTrueMonkey(self, trueMonkey) :
        self.trueMonkey = trueMonkey

    def setFalseMonkey(self, falseMonkey) :
        self.falseMonkey = falseMonkey

    def addItem(self, item : int):
        self.items.append(item)

    def inspectAndThrow(self) :
        if len(self.items) == 0 :
            return False

        item = self.items.pop(0)
        item = self.operation(item)
        # item = int(item / 3)

        if (item % self.test) == 0 :
            self.trueMonkey.addItem(item)
        else :
            self.falseMonkey.addItem(item)

        self.inspected += 1

        return True


if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", "-e", required=False)
    args = parser.parse_args()

    monkeys = []
    if args.example :
        print("Running example")

        # Setup Monkeys
        monkey0 = Monkey([79, 98], lambda x : x * 19, 23)
        monkey1 = Monkey([54, 65, 75, 74], lambda x : x + 6, 19)
        monkey2 = Monkey([79, 60, 97], lambda x : x * x, 13)
        monkey3 = Monkey([74], lambda x : x + 3, 17)

        # Who throws who
        monkey0.setTrueMonkey(monkey2)
        monkey0.setFalseMonkey(monkey3)

        monkey1.setTrueMonkey(monkey2)
        monkey1.setFalseMonkey(monkey0)

        monkey2.setTrueMonkey(monkey1)
        monkey2.setFalseMonkey(monkey3)

        monkey3.setTrueMonkey(monkey0)
        monkey3.setFalseMonkey(monkey1)

        monkeys = [monkey0, monkey1, monkey2, monkey3]
    else :
        print("Run Input")
        monkey0 = Monkey([63, 57],                      lambda x : x * 11,  7)
        monkey1 = Monkey([82, 66, 87, 78, 77, 92, 83],  lambda x : x + 1,   11)
        monkey2 = Monkey([97, 53, 53, 85, 58, 54],      lambda x : x * 7,   13)
        monkey3 = Monkey([50],                          lambda x : x + 3,   3)
        monkey4 = Monkey([64, 69, 52, 65, 73],          lambda x : x + 6,   17)
        monkey5 = Monkey([57, 91, 65],                  lambda x : x + 5,   2)
        monkey6 = Monkey([67, 91, 84, 78, 60, 69, 99, 83], lambda x : x * x, 5)
        monkey7 = Monkey([58, 78, 69, 65],              lambda x : x + 7,   19)

        monkey0.setTrueMonkey(monkey6)
        monkey0.setFalseMonkey(monkey2)

        monkey1.setTrueMonkey(monkey5)
        monkey1.setFalseMonkey(monkey0)

        monkey2.setTrueMonkey(monkey4)
        monkey2.setFalseMonkey(monkey3)

        monkey3.setTrueMonkey(monkey1)
        monkey3.setFalseMonkey(monkey7)

        monkey4.setTrueMonkey(monkey3)
        monkey4.setFalseMonkey(monkey7)

        monkey5.setTrueMonkey(monkey0)
        monkey5.setFalseMonkey(monkey6)

        monkey6.setTrueMonkey(monkey2)
        monkey6.setFalseMonkey(monkey4)

        monkey7.setTrueMonkey(monkey5)
        monkey7.setFalseMonkey(monkey1)

        monkeys = [monkey0, monkey1, monkey2, monkey3, monkey4, monkey5, monkey6, monkey7]

    for i in range(1000) :
        print(f"Round {i}")
        for monkey in monkeys:
            while monkey.inspectAndThrow():
                pass

    inspected_items = []
    for i, monkey in enumerate(monkeys):
        inspected_items.append(monkey.inspected)
        print(f"monkey{i} inspected {monkey.inspected} items")

    inspected_items.sort(reverse=True)

    print(f"Solution 1: {inspected_items [0] * inspected_items[1]}")

