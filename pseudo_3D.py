from platform import system
from platform import release
from math import sin
from math import cos
from math import ceil
if system() == "Windows":
    from msvcrt import getch
    if release() == "10":
        from colorama import init
        init()
else:
    import termios, fcntl, sys, os, time

def print_map(map_arr, loc):
    print("\033[H") # add end="" to start at the top of the screen
    for line in map_arr:
        print(line)
    print(f"\033[s\033[H\033[{round(loc[0])+1}B\033[{round(loc[1])}C@\033[u")

#def move(map_arr, loc, direction):
#    tmp = []
#    tmp.extend(loc)
#    tmp[0] += 0.25 * sin(direction)
#    tmp[1] += 0.25 * cos(direction)
#    if map_arr[ceil(tmp[0])][ceil(tmp[1])] != "#":
#        return(tmp)
#    else:
#        return(loc)
def move(map_arr, loc, key):
    tmp = []
    tmp.extend(loc)
    if key == "w":
        tmp[0] -= 1
    elif key == "s":
        tmp[0] += 1
    elif key == "a":
        tmp[1] -= 1
    elif key == "d":
        tmp[1] += 1
    if map_arr[tmp[0]][tmp[1]] != "#":
        return(tmp)
    else:
        return(loc)

def linux_get_ch():
    '''                                                                         
    Detects a key press and turns off echo in the terminal while active         
                                                                                
    Parameters                                                                  
    ----------                                                                  
    None.                                                                       
                                                                                
    Returns                                                                     
    -------                                                                     
    None.                                                                       
    '''                                                                         
    fd = sys.stdin.fileno()                                                     
                                                                                
    oldterm = termios.tcgetattr(fd)                                             
    newattr = termios.tcgetattr(fd)                                             
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO                   
    termios.tcsetattr(fd, termios.TCSANOW, newattr)                             
                                                                                
    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)                                   
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)                    
                                                                                
    try:                                                                        
        while True:                                                             
            time.sleep(0.05)                                                    
            try:                                                                
                c = sys.stdin.read(1)                                           
                if c:                                                           
                    return c                                                    
            except IOError: pass                                                
    finally:                                                                    
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)                       
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

def read_ch():
    if system() == "Windows":
        return(getch())
    else:
        return(linux_get_ch())

def deg_ch(direc):
    if direc > 360:
        return(0)
    elif direc < 0:
        return(360)
    else:
        return(direc)

def raycast(direction, map_arr, step, location):
    hit = []
    angle = deg_ch(direction - 45)
    mov = 0
    for _ in range(180):
        mov = 0.1
        for _ in range(100):
            if map_arr[ceil(location[0] + mov * sin(angle))][ceil(location[1] + mov * cos(angle))] == "#":
                print("ceil", ceil(location[0] + mov * sin(angle)), ceil(location[1] + mov * cos(angle)))
                print("cord", angle, mov)
                hit.append([angle, mov])
                break
            mov += 0.1
        angle = deg_ch(angle + step)
    print("hits", len(hit))
    print(hit)
    return(hit)

def line(dist):
    h = 48
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
    for i in range(0, 48):
        if i < start or i > end:
            stripe += " "
        else:
            stripe += "█"
    print("line", len(stripe))
    return(stripe)

def print_view(out):
    for j in range(48):
        for i in range(len(out)):
            print(out[i][j], end="")
        print()

def visual(direction, map_arr, location):
    step = 0.25
    hit = raycast(direction, map_arr, step, location)
    out = []
    angle = deg_ch(direction - 45)
    for _ in range(180):
        for ray in hit:
            if angle == ray[0]:
                print(ray[1])
                out.append(line(ray[1]))
        angle = deg_ch(angle + step)
    print_view(out)

def main():
    location = [1, 1]
    direction = 0
    map_arr = ["#########",
               "#       #",
               "#       #",
               "#       #",
               "#       #",
               "#       #",
               "#       #",
               "#       #",
               "#       #",
               "#########"]
    visual(direction, map_arr, location)
    print_map(map_arr, location)
    symb = read_ch()
    while symb != b"Q" and symb != "Q":
        print("direction", direction)
        if symb == b"w" or symb == "w":
            location = move(map_arr, location, "w")
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        elif symb == b"s" or symb == "s":
            location = move(map_arr, location, "s")
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        elif symb == b"a" or symb == "a":
            location = move(map_arr, location, "a")
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        elif symb == b"d" or symb == "d":
            location = move(map_arr, location, "d")
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        elif symb == b"q" or symb == "q":
            direction = deg_ch(direction + 1)
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        elif symb == b"e" or symb == "e":
            direction = deg_ch(direction - 1)
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        symb = read_ch()

if __name__ == "__main__":
    main()
