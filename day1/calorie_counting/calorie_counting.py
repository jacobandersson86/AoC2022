
# Part 1
elf = [0]
with open('./input/input.txt', 'r') as f:
    elf_count = 0
    for line in f.readlines():
        if line[:-1].isnumeric() == False:
            elf_count += 1
            elf.extend([int])
            elf[elf_count] = 0
        else :
            elf[elf_count] += int(line)

print(max(elf))

# Part 2
elf.sort(reverse=True)

total = sum([elf[0], elf[1], elf[2]])
print(total)
