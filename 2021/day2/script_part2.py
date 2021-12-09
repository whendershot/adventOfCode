f = open("input.txt", "r")

depth = 0
horizontal = 0
aim = 0
for line in f:
    line = line.strip()
    print(line)
    movement = line.split(" ")
    # print(movement)
    match movement[0]:
        case "forward":
            horizontal += int(movement[1])
            depth += int(movement[1]) * aim
        case "down":
            aim += int(movement[1])
        case "up":
            aim -= int(movement[1])
        case _: 
            print(f"{movement} was not handled; ignoring.")
    # print(f"Depth: {depth}, Horizontal position:{horizontal}, Aim {aim}")

f.close()
print(f"Z = {depth} * {horizontal} = {depth * horizontal}")
