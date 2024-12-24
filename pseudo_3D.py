# imports
try:
    from platform import system, release
    from math import sin, cos, ceil, pi
    if system() == "Windows":
        from msvcrt import getch
        if release() == "10":
            from colorama import init
            init()
    else:
        import tty, termios, fcntl, sys, os, time
except ImportError:
    print("Could not import necessary modules")
    raise ImportError

def print_map(map_arr, loc):
    '''
    print_map
    prints minimap in the top right corner

    Parameters
    ----------
    map_arr : list
        1D array of strings containing the map
    loc : list
        1D array that represents the player position on the map

    Returns
    -------
    new player location (tmp) after moving if it does not clip into a wall
    '''
    print("\033[H", end="") # add end="" to start at the top of the screen
    for line in map_arr:
        print(line)
    print(f"\033[H\033[{round(loc[0])}B\033[{round(loc[1])}C@\033[H\033[{len(map_arr)}B")

def move(map_arr, loc, direction, rot):
    tmp = []
    tmp.extend(loc)
    direction = rad_ch(direction, rot)
    tmp[0] += 0.25 * sin(direction * pi)
    tmp[1] += 0.25 * cos(direction * pi)
    if map_arr[ceil(tmp[0])][ceil(tmp[1])] != "#":
        return(tmp)
    else:
        return(loc)

def linux_get_ch():
    '''
    linux_get_ch
    Detects a key press and turns off echo in the terminal while active

    Parameters
    ----------
    None.

    Returns
    -------
    None.
    '''
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def read_ch():
    '''
    read_ch
    wrapper for running one of the functions depending on OS

    Parameters
    ----------
    None.

    Returns
    -------
    character inputted by the user
    '''
    if system() == "Windows":
        return(getch())
    else:
        return(linux_get_ch())

def rad_ch(direc, rot):
    '''
    rad_ch
    prevents the sum of direc and rot from going below 0 or over 2
    used for radians

    Parameters
    ----------
    direc : float
        current direction the camera is facing
    rot : float
        desired change to direc

    Returns
    -------
    |direc + rot| or (direc + rot - 2) to stay within the 0 <= x <= 2
    '''
    if direc + rot > 2:
        return(direc + rot - 2)
    elif direc + rot < 0:
        return(2 + direc + rot)
    else:
        return(direc + rot)

def raycast(direction, map_arr, step, location, length, shift):
    '''
    raycast
    casts rays each {step * pi} radians, records angle and distance for the rays
    moved

    Parameters
    ----------
    direction : float
        current direction the camera is facing
    map_arr : list
        1D array of strings containing the map
    step : float
        angle in radians for the intervals the rays are being cast at
    location : list
        1D array that represents the player position on the map
    length : int
        number of rays to be cast
    shift : float
        difference between direction and the angle for the first ray,
        realings the screen

    Returns
    -------
    hit : list
        list of lists containing the angle and distance travelled for each ray
    '''
    hit = []
    angle = rad_ch(direction, shift)
    mov = 0
    for _ in range(length):
        mov = 0.1
        for _ in range(100):
            if map_arr[ceil(location[0] + mov * sin(angle * pi))][ceil(location[1] + mov * cos(angle * pi))] == "#":
                hit.append([angle, mov])
                break
            mov += 0.1
        angle = rad_ch(angle, step)
    return(hit)

def line(dist, h):
    '''
    line
    creates stripes depending on how far away an object is

    Parameters
    ----------
    dist : float
        distance from the hit list in visual()
    h : int
        hight of the output in symbols

    Returns
    -------
    stripe : str
        a column of the future output
    '''
    if dist != 0:
        start = h /2 * (1 - 1 / dist)
    else:
        start = 0
    end = h / 2 * (1 + 1 / dist)
    if start < 0:
        start = 0
    if end > h:
        end = h - 1
    stripe = ""
    for i in range(h):
        if i < start:
            stripe += " "
        elif i > end:
            stripe += "::"
        else:
            if dist < 2:
                stripe += "█" # ░ ▒ ▓ █
            elif dist < 4:
                stripe += "▓" # ░ ▒ ▓ █
            elif dist < 6:
                stripe += "▒" # ░ ▒ ▓ █
            else:
                stripe += "░" # ░ ▒ ▓ █
    return(stripe)

def print_view(out, h, length):
    '''
    print_view
    outputs the {out}, rotating it 0.5pi radians 

    Parameters
    ----------
    out : list
        list of strings to be printed
    h : int
        hight of the output in symbols
    length : int
        length of each line to be printed

    Returns
    -------
    None.
    '''
    print("\033[A", end="")
    for j in range(h):
        for i in range(length):
            print(out[i][j], end="")
        print()
    print("\033[s")

def visual(direction, map_arr, location):
    '''
    visual
    creates and outputs the final image to the user
    direction : float
        current direction the camera is facing
    map_arr : list
        1D array of strings containing the map
    location : list
        1D array that represents the player position on the map

    Returns
    -------
    None.
    '''
    h = 38
    length = 160 # length * step must be equal to desired view angle in radians
    step = 0.003125
    shift = -0.25 # must be equal to - <desired view angle> / 2
    hit = raycast(direction, map_arr, step, location, length, shift)
    out = []
    angle = rad_ch(direction, shift)
    for _ in range(length):
        flag = True
        for ray in hit:
            if angle == ray[0]:
                flag = False
                out.append(line(ray[1], h))
        if flag:
            out.append(" " * int(h / 2) + "::" * int(h / 2))
        angle = rad_ch(angle, step)
    print_view(out, h, length)

def main():
    location = [1, 1]
    direction = 0
    map_arr = ["##########",
               "#        #",
               "#        #",
               "#  ##    #",
               "#   #    #",
               "#        #",
               "# #      #",
               "#    #   #",
               "#        #",
               "##########"]
    print(f"\033[H\033[0J\033[{len(map_arr)}B")
    visual(direction, map_arr, location)
    print_map(map_arr, location)
    symb = read_ch()
    while symb != b"Q" and symb != "Q":
        #print("direction", direction)
        if symb == b"w" or symb == "w":
            location = move(map_arr, location, direction, 0)
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        elif symb == b"s" or symb == "s":
            location = move(map_arr, location, direction, 1)
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        elif symb == b"a" or symb == "a":
            location = move(map_arr, location, direction, 1.5)
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        elif symb == b"d" or symb == "d":
            location = move(map_arr, location, direction, 0.5)
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        elif symb == b"q" or symb == "q":
            direction = rad_ch(direction, -0.05)
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        elif symb == b"e" or symb == "e":
            direction = rad_ch(direction, 0.05)
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        symb = read_ch()
    print("\033[u", end="")

if __name__ == "__main__":
    main()
