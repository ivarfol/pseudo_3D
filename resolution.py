from math import floor
while True:
    try:
        h = int(input("desired vertical resolution (must be divizible by 2): "))
    except:
        print("must be an integer!")
        continue
    if h % 2 != 0:
        print("must be divizible by two")
    else:
        break
while True:
    try:
        width = int(input("input horizontal resolution: "))
        break
    except:
        print("must be an integer!")
while True:
    try:
        length = int(input("desired true hirizontal resolution: "))
        break
    except:
        print("must be an integer!")
while True:
    try:
        fov = float(input("desired fov in pi radians: "))
        break
    except:
        print("must be a number!")
print("h =", h)
print("length =", length)
print("scale =", floor(width/length))
print("step =", fov / length)
print("shift =", -fov / 2)
