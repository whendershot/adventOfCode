f = open("D:\\Practice\\adventOfCode\\2021\\day1\\input.txt", "r")

prev_value = int(f.readline())
count_ascending  = 0
for line in f:
    next_value = int(line)
    if next_value > prev_value:
        count_ascending += 1
    prev_value = next_value

print(count_ascending)

f.close()