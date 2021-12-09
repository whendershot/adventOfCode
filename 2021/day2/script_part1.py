f = open("input.txt", "r")

depth = 0
horizontal = 0
for line in f:
    line = line.strip()
    print(line)
    movement = line.split(" ")
    # print(movement)
    match movement[0]:
        case "forward":
            horizontal += int(movement[1])
        case "down":
            depth += int(movement[1])
        case "up":
            depth -= int(movement[1])
        case _: 
            print(f"{movement} was not handled; ignoring.")

f.close()
print(f"Depth: {depth}, Horizontal position:{horizontal}")
print(f"Z = {depth} * {horizontal} = {depth * horizontal}")
