COORDINATE SYSTEM:

(x,y)
(0,0)
|------------------------------------------(x_max, y_max)
|					 |
|					 |
|					 |
|					 |
.					 .
.					 .
.					 .
.					 .
.					 .
.					 .
|					 |
|-------------------------------------------(x_max, y_max)
(0, y_max)

-makes use of PygAnimation Module from http://inventwithpython.com/pyganim/

-Currently:
-Have fish drawn and able to move using keyboard
-Graphics altered to fit our needs
-Fish size grows and picture stays preserved, to some extent, need to limit size of fish (design decision)
-Classes
Currently we have main.py and fish_artist.py
main.py -- handles all inputs and setting up, and does the final display update
fish_artist.py -- handles all response to keyboard inputs and drawing as needed
fish_artist can be used for other fish pictures, just need to vary parameters and take appropriate measures

Need to do:
- Handle several fish going across screen, possibly another class file for that?
- Handle collisions
- Need some sort of score counter
- Instructions for playing
- Buttons for starting, pausing and restarting
- Need to handle deaths, i.e when the main_fish collides with other bigger fish
- Need to handle background drawing 

