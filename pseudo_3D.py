# imports
try:
    import sys
    from time import sleep
    from platform import system, release
    from math import sin, cos, ceil, pi, floor, acos, sqrt, asin
    from pygame.locals import*
    import pygame
    if system() == "Windows":
        if release() == "10":
            from colorama import init
            init()
except ImportError:
    print("Could not import necessary modules")
    raise ImportError

def move(map_arr, loc, direction, rot, mod, noclip):
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
    if ceil(tmp[0]) < len(map_arr)-1 and ceil(tmp[0]) > 0 and ceil(tmp[1]) < len(map_arr[ceil(tmp[0])])-1 and ceil(tmp[1]) > 0 and (map_arr[ceil(tmp[0])][ceil(tmp[1])] != "#" or noclip):
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

def raycast(direction, map_arr, location, length, shift, base_angles, side):
    '''
    raycast
    casts rays, records angle and distance for the rays
    moved

    Parameters
    ----------
    direction : float
        current direction the camera is facing
    map_arr : list
        1D array of strings containing the map
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
    _angle = rad_ch(direction, shift)
    ox, oy = location[1], location[0]
    x_map, y_map = int(location[1]), int(location[0])
    for j in range(length):
        angle = rad_ch(_angle + acos((side - j * cos(base_angles * pi)) / sqrt(side ** 2 + j ** 2 - 2 * side * j * cos(base_angles * pi))) / pi, 0)
        sin_a = sin(angle * pi)
        cos_a = cos(angle * pi)
        if sin_a == 0:
            sin_a = 1e-6
        elif cos_a == 0:
            cos_a = 1e-6
        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(20):
            tile_hor = floor(x_hor)+1, floor(y_hor)+1
            if tile_hor[1] > 9 or tile_hor[0] > 50 or tile_hor[1] < 1 or tile_hor[0] < 1 or map_arr[tile_hor[1]][tile_hor[0]] == "#":
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(20):
            tile_vert = floor(x_vert)+1, floor(y_vert)+1
            if tile_vert[1] > 9 or tile_vert[0] > 50 or tile_vert[1] < 1 or tile_vert[0] < 1 or map_arr[tile_vert[1]][tile_vert[0]] == "#":
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth
        if depth_vert < depth_hor:
            hit.append([angle, depth_vert])
        else:
            hit.append([angle, depth_hor])
    return(hit)

def line(dist, h, i, screen, scale, perp_dist):
    '''
    line
    creates stripes depending on how far away an object is

    Parameters
    ----------
    dist : float
        distance from the hit list in visual()
    h : int
        hight of the output in symbols
    i : int
        horizontal position on the screen
    screen : 
        screen from pyame
    line_color : tup
        tuple with line color
    scale : int
        how scaled up the output is

    Returns
    -------
    stripe : str
        a column of the future output
    '''
    if dist != 0:
        start = h / 2 * (1 - 1 / perp_dist)
        end = h / 2 * (1 + 1 / perp_dist)
    else:
        start = 0
        end = h - 1
    if start < 0:
        start = 0
    if end > h:
        end = h - 1
    if dist <=20:
        line_color = (200-dist*10, 200-dist*10, 200-dist*10)
    else:
        line_color = (0, 0, 0)
    pygame.draw.line(screen, line_color, (i * scale, round(start)), (i * scale, round(end)), scale)

def print_view(map_arr, direction, location, hit, screen):
    '''
    print_view
    prints the map

    Parameters
    ----------
    map_arr : list
        1D array of strings containing the map
    direction : float
        current direction the camera is facing
    location : list
        1D array that represents the player position on the map
    '''
    line_color = (0, 0, 255)
    ray_color = (255, 0, 0)
    for line_num in range(len(map_arr)):
        for symbol_num in range(len(map_arr[line_num])):
            if map_arr[line_num][symbol_num] == "#":
                pygame.draw.rect(screen, line_color, pygame.Rect(symbol_num*10, line_num*10, 10, 10))
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(round(location[1]*10)+7, round(location[0]*10)+7, 6, 6))
    for ray in hit:
        pygame.draw.line(screen, ray_color, (round(location[1]*10)+10, round(location[0]*10)+10), (ceil((location[1] + ray[1]*cos(ray[0]*pi))*10+10), ceil((location[0] + ray[1]*sin(ray[0]*pi))*10+10)))
    #print(f"direction: {direction:.3f}\nlocation: {location[1]:.3f}x {location[0]:.3f}y")

def visual(direction, map_arr, location, length, h, screen, screen_color, scale, show_map, noclip, shift, base_angles, side):
    '''
    visual
    creates and outputs the final image to the user
    direction : float
        current direction the camera is facing
    map_arr : list
        1D array of strings containing the map
    location : list
        1D array that represents the player position on the map
    length : int
        length of the screen
    h : int
        hight of the screen
    screen : 
        screen from pyame
    line_color : tup
        tuple with line color
    sceen_color : tup
        tuple with screen color
    scale : int
        how scaled up the output is

    Returns
    -------
    None.
    '''
    hit = raycast(direction, map_arr, location, length, shift, base_angles, side)
    screen.fill(screen_color)
    for i in range(length):
        line(hit[i][1], h, i, screen, scale, hit[i][1] * cos(rad_ch(rad_ch(direction - hit[i][0], 0), 0) * pi))
    if show_map:
        print_view(map_arr, direction, location, hit, screen)
    if noclip:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(length*scale-30, h-30, 20, 20))
    pygame.display.flip()

def main():
    length = 200
    h = 500
    scale = 5
    screen_color = (0, 0, 0)
    line_color = (255, 255, 255)
    screen=pygame.display.set_mode((length*scale,h))
    screen.fill(screen_color)
    pygame.display.flip()
    location = [1, 1]
    direction = 0
    show_map = False
    noclip = False
    map_arr = ["###################################################",
               "#               #                                 #",
               "#               #        #                        #",
               "#  ##    ##########      #                        #",
               "#   #             #      #                        #",
               "#  #     ######## ### ####                        #",
               "# #      ####     #      #                        #",
               "#    #      # #####      #                        #",
               "#        ## #            #                        #",
               "###################################################"]
    move_tic = 0
    mod = 0.5
    shift = -0.25 # must be equal to - <desired view angle> / 2
    base_angles = rad_ch(0.5, shift)
    side = length * sin(base_angles * pi) / sin(shift * -2 * pi)
    visual(direction, map_arr, location, length, h, screen, screen_color, scale, show_map, noclip, shift, base_angles, side)
    while True:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if show_map:
                        show_map = False
                    else:
                        show_map = True
                    visual(direction, map_arr, location, length, h, screen, screen_color, scale, show_map, noclip, shift, base_angles, side)
                elif event.key == pygame.K_n:
                    if noclip:
                        noclip = False
                    else:
                        noclip = True
                    visual(direction, map_arr, location, length, h, screen, screen_color, scale, show_map, noclip, shift, base_angles, side)
        if keys[K_x] and keys[K_LSHIFT]:
            sys.exit(0)
        if move_tic == 0: 
            if keys[K_LSHIFT]:
                mod = 2
            elif keys[K_LCTRL]:
                mod = 0.5
            if keys[K_w] and not keys[K_s]:
                location = move(map_arr, location, direction, 0, mod, noclip)
                move_tic = 1
            elif keys[K_s] and not keys[K_w]:
                location = move(map_arr, location, direction, 1, mod, noclip)
                move_tic = 1
            if keys[K_a] and not keys[K_d]:
                location = move(map_arr, location, direction, 1.5, mod, noclip)
                move_tic = 1
            elif keys[K_d] and not keys[K_a]:
                location = move(map_arr, location, direction, 0.5, mod, noclip)
                move_tic = 1
            if keys[K_q] and not keys[K_e]:
                direction = rad_ch(direction, -0.025 * mod)
                move_tic = 1
            elif keys[K_e] and not keys[K_q]:
                direction = rad_ch(direction, 0.025 * mod)
                move_tic = 1
            if move_tic == 1:
                visual(direction, map_arr, location, length, h, screen, screen_color, scale, show_map, noclip, shift, base_angles, side)
            mod = 1
        if move_tic > 0:
            move_tic -= 1
            sleep(0.025)

if __name__ == "__main__":
    main()
