# Pseudo 3D
## Overview
This is a raycasting implimentation written in python.  
It uses pygame for reading user inputs and outputting the screen
## Modifying
In the main()  
h - is the hight of the screen in pixels
length - is the length of the screen in pixels  
scale - is how much the actual picture is upscaled when outputting it  
  
In the visual()  
step - is the angle in pi radians the rays are being cast at  
shift - is the view angle / 2, centeres the screen  
the following values can be assigned for a 80x43 resolution:  
I recommend keeping the pre set values, but you can change them  
if you want, the program resolution.py can be used to prevent check the validity  
of your values  
you can replace the h, length and scale into the main()
and step, shift in the visual() functions

## Controls
wasd - move forward, left, back or right  
qe - rotate camera left or right  
Lshift increaces the speed by x2  
Lctrl decreaces the speed by x0.5  
Lshift+x exits the game
