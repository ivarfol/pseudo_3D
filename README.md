# Pseudo 3D
## Overview
This is a raycasting implimentation written in python.  
It outputs the level as a combination of the following symbols without quotes  
" ░▒▓█:" the ":" is used for floor, and the rest for different distances to  
the walls.  
The program uses ascii escape codes for cursor control.  
## Modifying
If the game looks like this:  
```
##########██████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                             
#@       #                        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████ 
#        #██████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒                       
#  ##    #                        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████  
#   #    #██████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒░                  
#        #                        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████  
# #      #██████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░  
#    #   #░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████  
#        #██████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░  
##########░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████  
████████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░  
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████  
████████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░  
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████  
████████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░  
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████  
████████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒░::::::::::::::::  
::::::::::::::::::::::::::::::::::▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████  
████████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒:::::::::::::::::::::  
::::::::::::::::::::::::::::::::::▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████  
████████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓:::::::::::::::::::::::::::  
::::::::::::::::::::::::::::::::::▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████  
████████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓:::::::::::::::::::::::::::::::::  
::::::::::::::::::::::::::::::::::▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████  
████████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓::::::::::::::::::::::::::::::::::::::  
:::::::::::::::::::::::::::::::::::::::▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████████████████████  
████████████████████████▓▓▓▓▓▓▓▓▓▓▓:::::::::::::::::::::::::::::::::::::::::::::  
::::::::::::::::::::::::::::::::::::::::::::::▓▓▓▓▓▓▓▓▓▓▓███████████████████████  
```
This is caused by a low horizontal resolution in symbols  
It can be fixed by editing values in the visual() function  
h - is the hight of the screen in symbols  
length - is the length of the screen in pixels  
step - is the angle in pi radians the rays are being cast at  
the following values can be assigned for a 80x43 resolution:  
h = 43 - len(map\_arr)  
length = 80  
step = 0.00625  
this would look like this:  
``##########``  
``#@       #``  
``#        #``  
``#  ##    #``  
``#   #    #``  
``#        #``  
``# #      #``  
``#    #   #``  
``#        #``  
``##########``  
````  
````  
````  
````  
````  
````  
``███                                                                           ██``  
``████████                                                                 ███████``  
``████████████                                                         ███████████``  
``████████████▓▓▓                                                   ▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓                                         ▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓                                   ▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓                               ▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒                           ▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒░                        ▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒░::::::::::::::::::::::::▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒:::::::::::::::::::::::::::▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓:::::::::::::::::::::::::::::::▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓:::::::::::::::::::::::::::::::::::▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓:::::::::::::::::::::::::::::::::::::::::▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓:::::::::::::::::::::::::::::::::::::::::::::::::::▓▓▓███████████``  
``████████████:::::::::::::::::::::::::::::::::::::::::::::::::::::::::███████████``  
``████████:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::███████``  
``███:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::██``  
``::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::``  
``::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::``  
``::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::``  
``::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::``  
``::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::``  
You can also remove "\\033[{len(map\_arr)}B" from lines 19 and 161 and put the  
following values in visual()  
h = 24  
length = 80  
step = 0.00625  
To output the map over the picture, this would look like this:  
##########                                                                      ``  
``#@       #                                                                      ``  
``#        #                                                                      ``  
``#  ##    #                                                                      ``  
``#   #    #                                                                      ``  
``#        #                                                               ███████``  
``# #      #██                                                         ███████████``  
``#    #   #██▓▓▓▓▓▓                                             ▓▓▓▓▓▓███████████``  
``#        #██▓▓▓▓▓▓▓▓▓▓▓                                   ▓▓▓▓▓▓▓▓▓▓▓███████████``  
``##########██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                              ▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒                         ▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒:::::::::::::::::::::::::▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒:::::::::::::::::::::::::::::▓▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓▓▓▓▓:::::::::::::::::::::::::::::::::::▓▓▓▓▓▓▓▓▓▓▓███████████``  
``████████████▓▓▓▓▓▓▓:::::::::::::::::::::::::::::::::::::::::::▓▓▓▓▓▓▓███████████``  
``████████████▓▓:::::::::::::::::::::::::::::::::::::::::::::::::::::▓▓███████████``  
``████████:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::███████``  
``███:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::██``  
``::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::``  
``::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::``  
``::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::``  
Be warned, this coases flickering on the minimap when moving  
## Controls
wasd - move forward, left, back or right  
qe - rotate camera left or right  
