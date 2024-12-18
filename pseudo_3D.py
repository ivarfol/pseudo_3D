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

def move(map_arr, loc, direction):
    tmp = []
    tmp.extend(loc)
    tmp[0] += 0.25 * sin(direction)
    tmp[1] += 0.25 * cos(direction)
    if map_arr[ceil(tmp[0])][ceil(tmp[1])] != "#":
        print_map(map_arr, tmp)
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

def main():
    location = [1, 1]
    direction = 0
    map_arr = ["#########",
               "#    #  #",
               "#       #",
               "# ###   #",
               "#       #",
               "# # #####",
               "#       #",
               "#   ##  #",
               "#       #",
               "#########"]
    print_map(map_arr, location)
    symb = read_ch()
    while symb != b"Q" and symb != "Q":
        if symb == b"w" or symb == "w":
            location = move(map_arr, location, direction)
        elif symb == b"s" or symb == "s":
            location = move(map_arr, location, direction + 180)
        elif symb == b"a" or symb == "a":
            location = move(map_arr, location, direction + 90)
        elif symb == b"d" or symb == "d":
            location = move(map_arr, location, direction + 270)
        elif symb == b"q" or symb == "q":
            direction -= 1
        elif symb == b"e" or symb == "e":
            direction += 1
        symb = read_ch()

if __name__ == "__main__":
    main()
