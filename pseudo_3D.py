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

def move(map_arr, loc, direction, rot):
    tmp = []
    tmp.extend(loc)
    direction = deg_ch(direction, rot)
    tmp[0] += 0.25 * sin(direction)
    tmp[1] += 0.25 * cos(direction)
    if map_arr[ceil(tmp[0])][ceil(tmp[1])] != "#":
        return(tmp)
    else:
        return(loc)
#def move(map_arr, loc, key):
#    tmp = []
#    tmp.extend(loc)
#    if key == "w":
#        tmp[0] -= 1
#    elif key == "s":
#        tmp[0] += 1
#    elif key == "a":
#        tmp[1] -= 1
#    elif key == "d":
#        tmp[1] += 1
#    if map_arr[tmp[0]][tmp[1]] != "#":
#        return(tmp)
#    else:
#        return(loc)

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

def deg_ch(direc, rot):
    if direc + rot > 37.6:
        return(direc + rot - 37.6)
    elif direc + rot < 0:
        return(37.6 + direc + rot)
    else:
        return(direc + rot)

def raycast(direction, map_arr, step, location, length):
    hit = []
    angle = deg_ch(direction, -45)
    mov = 0
    for _ in range(length):
        mov = 0.1
        for _ in range(100):
            if map_arr[ceil(location[0] + mov * sin(angle))][ceil(location[1] + mov * cos(angle))] == "#":
                #print("ceil", ceil(location[0] + mov * sin(angle)), ceil(location[1] + mov * cos(angle)))
                #print("cord", angle, mov)
                hit.append([angle, mov])
                break
            mov += 0.1
        angle = deg_ch(angle, step)
    #print("hits", len(hit))
    #print(hit)
    return(hit)

def line(dist, h):
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
    #print("line", len(stripe))
    return(stripe)

def print_view(out, h, length):
    for j in range(h):
        for i in range(length):
            print(out[i][j], end="")
        print()

def visual(direction, map_arr, location):
    h = 48
    length = 160
    step = 0.01
    hit = raycast(direction, map_arr, step, location, length)
    out = []
    angle = deg_ch(direction, -45)
    for _ in range(length):
        flag = True
        for ray in hit:
            if angle == ray[0]:
                flag = False
                #print(ray[0], angle)
                out.append(line(ray[1], h))
        if flag:
            out.append(" " * int(h / 2) + "::" * int(h / 2))
        angle = deg_ch(angle, step)
    print_view(out, h, length)

def main():
    location = [1, 1]
    direction = 1
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
    print("\n\n\n")
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
            location = move(map_arr, location, direction, 9.4)
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        elif symb == b"a" or symb == "a":
            location = move(map_arr, location, direction, 4.7)
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        elif symb == b"d" or symb == "d":
            location = move(map_arr, location, direction, 14.1)
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        elif symb == b"q" or symb == "q":
            direction = deg_ch(direction, -0.1)
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        elif symb == b"e" or symb == "e":
            direction = deg_ch(direction, 0.1) # 52.4 - 90 - full rotation
            visual(direction, map_arr, location)
            print_map(map_arr, location)
        symb = read_ch()

if __name__ == "__main__":
    main()
