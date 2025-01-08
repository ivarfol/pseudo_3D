# imports
try:
    import sys
    from time import sleep
    from platform import system, release
    from math import sin, cos, ceil, pi
    from pygame.locals import*
    import pygame
    if system() == "Windows":
        if release() == "10":
            from colorama import init
            init()
except ImportError:
    print("Could not import necessary modules")
    raise ImportError

def move(map_arr, loc, direction, rot, mod):
    '''
    move
    function for moving the player
    map_arr : list
        1D array of strings containing the map
    loc : list
        1D array that represents the player position on the map
    direction : float
        current direction the camera is facing
    rot : float
        desired change to direc
    '''
    tmp = []
    tmp.extend(loc)
    direction = rad_ch(direction, rot)
    tmp[0] += 0.125 * sin(direction * pi) * mod
    tmp[1] += 0.125 * cos(direction * pi) * mod
    if map_arr[ceil(tmp[0])][ceil(tmp[1])] != "#":
        return(tmp)
    else:
        return(loc)

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
    if direc + rot >= 2:
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

def line(dist, h, i, screen, line_color):
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
        start = h / 2 * (1 - 1 / dist)
        end = h / 2 * (1 + 1 / dist)
    else:
        start = 0
        end = h - 1
    if start < 0:
        start = 0
    if end > h:
        end = h - 1
    pygame.draw.line(screen, line_color, (i * 5, round(start)), (i * 5, round(end)), 5)

def print_view(map_arr, direction, location):
    output = "\033[u"
    for line_num in range(len(map_arr)):
        output += map_arr[line_num]
        if line_num == 0:
            output += f" direction: {direction:.3f}"
        elif line_num == 1:
            output += f" location: {location[1]:.3f}x {location[0]:.3f}y"
        output += "\n"
    output += f"\033[u\033[{round(location[0])}B\033[{round(location[1])}C@\033[u\033[{len(map_arr)}B"
    print(output, end="")

def visual(direction, map_arr, location, length, h, screen, line_color, screen_color):
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
    # length * step must be equal to desired view angle in radians
    step = 0.0025
    shift = -0.25 # must be equal to - <desired view angle> / 2
    hit = raycast(direction, map_arr, step, location, length, shift)
    out = []
    angle = rad_ch(direction, shift)
    screen.fill(screen_color)
    for i in range(length):
        for ray in hit:
            if angle == ray[0]:
                line(ray[1], h, i, screen, line_color)
        angle = rad_ch(angle, step)
    pygame.display.flip()
    print_view(map_arr, direction, location)

def main():
    print("\033[s", end="")
    length = 200
    h = 500
    screen_color = (0, 0, 0)
    line_color = (255, 255, 255)
    screen=pygame.display.set_mode((length*5,h))
    screen.fill(screen_color)
    #pygame.draw.line(screen,line_color, (60, 80), (130, 100))
    pygame.display.flip()
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
    #print(f"\033[H\033[0J\033[{len(map_arr)}B")
    visual(direction, map_arr, location, length, h, screen, line_color, screen_color)
    move_tic = 0
    mod = 0.5
    while True:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
        if keys[K_x] and keys[K_LSHIFT]:
            sys.exit(0)
        if move_tic == 0: 
            if keys[K_LSHIFT]:
                mod = 2
            elif keys[K_LCTRL]:
                mod = 0.5
            if keys[K_w]:
                location = move(map_arr, location, direction, 0, mod)
                visual(direction, map_arr, location, length, h, screen, line_color, screen_color)
                move_tic = 5
            elif keys[K_s]:
                location = move(map_arr, location, direction, 1, mod)
                visual(direction, map_arr, location, length, h, screen, line_color, screen_color)
                move_tic = 5
            elif keys[K_a]:
                location = move(map_arr, location, direction, 1.5, mod)
                visual(direction, map_arr, location, length, h, screen, line_color, screen_color)
                move_tic = 5
            elif keys[K_d]:
                location = move(map_arr, location, direction, 0.5, mod)
                visual(direction, map_arr, location, length, h, screen, line_color, screen_color)
                move_tic = 5
            elif keys[K_q]:
                direction = rad_ch(direction, -0.025 * mod)
                visual(direction, map_arr, location, length, h, screen, line_color, screen_color)
                move_tic = 5
            elif keys[K_e]:
                direction = rad_ch(direction, 0.025 * mod)
                visual(direction, map_arr, location, length, h, screen, line_color, screen_color)
                move_tic = 5
            mod = 1
        if move_tic > 0:
            move_tic -= 1
            sleep(0.005)

if __name__ == "__main__":
    main()
