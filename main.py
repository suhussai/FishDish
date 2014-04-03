import pygame
from pygame.locals import *
import sys
import math
import time
import random
from random import randint
right = 'right'
left = 'left'


'''
useful links:

http://shinylittlething.com/2009/07/22/pygame-and-animated-sprites-take-2/

http://thepythongamebook.com/en:pygame:step016

https://www.pygame.org/docs/ref/surface.html

https://www.pygame.org/docs/ref/rect.html#pygame.Rect.union

http://dr0id.homepage.bluewin.ch/pygame_tutorial01.html#optimizations

http://www.pygame.org/docs/tut/newbieguide.html

'''
def add_a_new_cpu(screen, available_sprites):
    Stype = random.choice(available_sprites)
    position = get_a_corner(screen)
    new = cpu_Fish(screen, Stype, right, random.uniform(0.1,1.0), position[0], position[1])
    #print(new.get_f_x(), new.get_f_y())
    return new

def get_a_corner(screen):
    edges = ['left','right','top','bottom']
    edge = random.choice(edges)
    print(edge)
    rv = None
    if edge == 'left':
        rv = [0, randint(0,300)]
    elif edge == 'right':
        rv = [400,randint(0,300)]
        #rv = [200,200]
    elif edge == 'top':
        rv = [randint(0,400),0]
    elif edge == 'bottom':
        rv = [randint(0,400), 300]
    return rv

def deg_to_rad(deg):
    rad = (deg/180) * math.pi
    return rad


def squeeze(num, max_num, min_num):
    '''
    squeezes a number between the max_num and the min_num
    useful for bounds checking
    
    >>> squeeze(50, 10, 4)
    10
    >>> squeeze(-20, 10, 4)
    4
    '''
    if num < min_num:
        num = min_num
    if num > max_num:
        num = max_num
    return num

class cpu_Fish(pygame.sprite.Sprite):
    
    def __init__(self, screen, fish_name, directionTo, fish_speed = 10, x = 0, y = randint(50,200), fish_width = 0, fish_height = 0):
        #special note to the random generation of the y position
        #as it is right now, it should generate a cpu fish at some y position between 100,300

        #initialze important variables
        #screen so we can blit in our class
        #onto the main screen
        self.screen = screen
        
        #we use the same fish naming standards as before
        self.f_n = fish_name
        
        #rate of movement of fish
        self.f_s = fish_speed


        self.fish_direction = directionTo
        
        #starting x and y for fish
        '''
        if self.fish_direction == right:
            self.f_x = 0
        elif self.fish_direction == left:
            self.f_x = windowSize[0]
            '''
        self.f_x = x
        self.f_y = y

        self.vector = randint(0,360) #Pick a random direction (in degrees)
        if self.vector >= 90 and self.vector <= 270:
            self.fish_direction = right #everything is backwards (keep in mind)
        else:
            self.fish_direction = left


        #starting width and height of fish
        self.f_h = fish_height
        self.f_w = fish_width

        
        pygame.sprite.Sprite.__init__(self)


        # load up all frames 
        # start by loading in the five left frames
        # then to get right, we simply flip them 
        a = pygame.image.load('fishdish/' + str(self.f_n) + '_left_1.png').convert_alpha()
        b = pygame.image.load('fishdish/' + str(self.f_n) + '_left_2.png').convert_alpha()                  
        c = pygame.image.load('fishdish/' + str(self.f_n) + '_left_3.png').convert_alpha()
        d = pygame.image.load('fishdish/' + str(self.f_n) + '_left_4.png').convert_alpha()
        e = pygame.image.load('fishdish/' + str(self.f_n) + '_left_5.png').convert_alpha()
        self.lfish_frame = [a,b,c,d,e]

        self.rfish_frame = [pygame.transform.flip(a, True, False),
                            pygame.transform.flip(b, True, False),
                            pygame.transform.flip(c, True, False),
                            pygame.transform.flip(d, True, False),
                            pygame.transform.flip(e, True, False)]

        #set width and height according to img width and height
        self.f_h = a.get_height()
        self.f_w = a.get_width()
#        print(self.f_h)
#        print(self.f_w)


        self.fish_frame_num = 0 #initialize fish frame count to zero


        #0-4 - first five frames for right facing fish
        #5-9 - second five frames for left facing fish
        self.fish_main_surf = []

        for frame in self.rfish_frame:
            self.fish_main_surf.append(frame)
        for frame in self.lfish_frame:
            self.fish_main_surf.append(frame)

        self.fish_main_rect = self.fish_main_surf[0].get_rect()

    def get_f_y(self):
        return self.f_y
    def get_f_x(self):
        return self.f_x

    def update(self):
        #cpu fish direction is either from left to right
        #or right to left
        # 1: from left to right
        # 2: from right to left

        #clear up old image
        bg2 = pygame.image.load(main_bg_file)
#        print(bg2.get_width())
#        print(bg2.get_height())
#        bg2.fill((255,0,0)) #fills dirty with red to color to show how large rect is 

        #blit 

        if self.fish_main_rect.bottomright[0] >= windowSize[0]:
            dirtyrect1 = bg2.subsurface((self.fish_main_rect[0], self.fish_main_rect[1], windowSize[0] - self.fish_main_rect[0], self.fish_main_rect[3]))
        
        else:
            dirtyrect1 = bg2.subsurface(self.fish_main_rect)
            
        rl.append(self.screen.blit(dirtyrect1, (self.f_x, self.f_y)))


        d = self.fish_direction
#        print(d)
#        print("the above is the way the fish is going ")
        self.f_x -= self.f_s * math.cos( (deg_to_rad(self.vector)))
        self.f_y -= self.f_s * math.sin( (deg_to_rad(self.vector)))

        #print(self.f_x,self.f_y)
            
#        self.f_x = squeeze(self.f_x, windowSize[0] - self.f_w*2, self.f_w)
#        self.f_y = squeeze(self.f_y, windowSize[1] - self.f_h*2, self.f_h)
        self.fish_main_rect.topleft = (self.f_x, self.f_y)

        self.blito()
            

    def blito(self):
        #displays the main_rect fish frame and handles the updating of the frame count
        #at the topleft coordinates of the fish_rect of the instance of the fish

        if self.fish_direction == right:
            self.fish_frame_num += 1
            if self.fish_frame_num >= 5:
                self.fish_frame_num = 0 #first right facing frame

        elif self.fish_direction == left:
            self.fish_frame_num += 1
            if self.fish_frame_num >= 9:
                self.fish_frame_num = 5 #first right facing frame

        bg2 = pygame.image.load(main_bg_file)
#        bg2.fill((255,0,0)) #fills dirty with red to color to show how large rect is 
        #dirty rect calc to get dimensions of the background the sprite messed up
        # calculate clean rect

        #the cpu fish is gonna skip through the whole screen so...
#        print(abs(self.f_x - self.f_w//2) + abs(self.f_w*2))
#        print(abs(self.f_y - self.f_h//2) + abs(self.f_w*2))
#        print(windowSize)


        if (self.f_x > windowSize[0] + 50):
            #fish is gawwn dude ...to the right
            if cpu_fishes.has(self):
                #kill the sprite!!!
                cpu_fishes.remove(self)
        '''
        
        if (self.f_x < windowSize[0] - 50):
            #fish is gawwn dude ...to the left
            if cpu_fishes.has(self):
                #kill the sprite!!!
                cpu_fishes.remove(self)

        '''

#        if (self.f_x +  self.f_w*2) >= windowSize[0]:
            # a right going fish that needs to cross the boundary max width of screen

#            dirtyrect = bg2.subsurface((abs(self.f_x), abs(self.f_y - self.f_h//2), windowSize[0] - abs(self.f_x - self.f_w//2), abs(self.f_h*2)))

#        elif (abs(self.f_y - self.f_w//2) +  abs(self.f_w*2)) <= 0 or self.f_x == 0:
            # a left going fish that needs to cross the boundary min width of screen i.e 0
#            dirtyrect = bg2.subsurface((0, abs(self.f_y - self.f_h//2), abs(self.f_w*2),abs(self.f_h*2))) 
#        elif self.f_x == 0:
#            dirtyrect = bg2.subsurface((0,
        
        #        else:
            #for right or left going fish that needs normal dirty rect caluculating
#            dirtyrect = bg2.subsurface((abs(self.f_x - self.f_w//2), abs(self.f_y - self.f_h//2), abs(self.f_w*2), abs(self.f_h*2))) 
#        print([(abs(self.f_x - self.f_w//2), abs(self.f_y - self.f_h//2), abs(self.f_w*2), abs(self.f_h*2))])

        # we need to do some editions to the fish rect when calculating the dirty rect around 
        # this is to ensure that no traces of the fish get eft on
        # and then we blit it on before the sprite
#        self.screen.blit(dirtyrect, (self.fish_main_rect.topleft[0] - self.f_w//2, self.fish_main_rect.topleft[1] - self.f_h//2))
        # blit clean rect on top of "dirty" screen

        self.fish_main_rect = self.screen.blit(self.fish_main_surf[self.fish_frame_num], self.fish_main_rect.topleft) #update pos of fis
        rl.append(self.fish_main_rect)

#        print("done updating cpu fish")
#        print(self.f_n)


#drawing going to be done in 3 three 
class Fish(pygame.sprite.Sprite):
    
    def __init__(self,screen,  fish_name, fish_speed = 10, x = 200, y = 200, fish_width = 0, fish_height = 0):


        #initialze important variables
        #screen so we can blit in our class
        #onto the main screen
        self.screen = screen
        
        #we use the same fish naming standards as before
        self.f_n = fish_name
        
        #rate of movement of fish
        self.f_s = fish_speed
        
        #starting x and y for fish
        self.f_x = x
        self.f_y = y

        #starting width and height of fish
        self.f_h = fish_height
        self.f_w = fish_width

        
        pygame.sprite.Sprite.__init__(self)


        # load up all frames 
        # start by loading in the five left frames
        # then to get right, we simply flip them 
        a = pygame.image.load('fishdish/' + str(self.f_n) + '_left_1.png').convert_alpha()
        b = pygame.image.load('fishdish/' + str(self.f_n) + '_left_2.png').convert_alpha()                  
        c = pygame.image.load('fishdish/' + str(self.f_n) + '_left_3.png').convert_alpha()
        d = pygame.image.load('fishdish/' + str(self.f_n) + '_left_4.png').convert_alpha()
        e = pygame.image.load('fishdish/' + str(self.f_n) + '_left_5.png').convert_alpha()
        self.lfish_frame = [a,b,c,d,e]

        self.rfish_frame = [pygame.transform.flip(a, True, False),
                            pygame.transform.flip(b, True, False),
                            pygame.transform.flip(c, True, False),
                            pygame.transform.flip(d, True, False),
                            pygame.transform.flip(e, True, False)]

        #set width and height according to img width and height
        self.f_h = a.get_height()
        self.f_w = a.get_width()
        print(self.f_h)
        print(self.f_w)


        self.fish_frame_num = 0 #initialize fish frame count to zero
        self.fish_direction = right #initialize the direction of the fish to be facing right
        #0-4 - first five frames for right facing fish
        #5-9 - second five frames for left facing fish
        self.fish_main_surf = []

        for frame in self.rfish_frame:
            self.fish_main_surf.append(frame)
        for frame in self.lfish_frame:
            self.fish_main_surf.append(frame)

        self.fish_main_rect = self.fish_main_surf[0].get_rect()


    def update(self, direction_of_movement = 0):
        # direction == 0 no movement
        # direction == 1 right
        # direction == 2 left
        # direction == 3 up
        # direction == 4 down

        #clear up old image
        bg2 = pygame.image.load(main_bg_file)
#        bg2.fill((255,0,0)) #fills dirty with red to color to show how large rect is 

        #blit 
        dirtyrect1 = bg2.subsurface(self.fish_main_rect)
        rl.append(self.screen.blit(dirtyrect1, (self.f_x, self.f_y)))



        d = direction_of_movement
        if d == 1:
            self.f_x += self.f_s
        elif d == 2:
            self.f_x -= self.f_s
        elif d == 3:
            self.f_y -= self.f_s
        elif d == 4:
            self.f_y += self.f_s


        self.f_x = squeeze(self.f_x, windowSize[0] - self.f_w*2, self.f_w)
        self.f_y = squeeze(self.f_y, windowSize[1] - self.f_h*2, self.f_h)
        self.fish_main_rect.topleft = (self.f_x, self.f_y)

        self.blito()
            

    def blito(self):
        #displays the main_rect fish frame and handles the updating of the frame count
        #at the topleft coordinates of the fish_rect of the instance of the fish

        if self.fish_direction == right:
            self.fish_frame_num += 1
            if self.fish_frame_num >= 5:
                self.fish_frame_num = 0 #first right facing frame

        elif self.fish_direction == left:
            self.fish_frame_num += 1
            if self.fish_frame_num >= 9:
                self.fish_frame_num = 5 #first right facing frame

        bg2 = pygame.image.load(main_bg_file)
#        bg2.fill((255,0,0)) #fills dirty with red to color to show how large rect is 

        #blit 
#        dirtyrect1 = bg2.subsurface(self.fish_main_rect)
#        self.screen.blit(dirtyrect1, (self.f_x, self_f_y))
        #dirty rect calc to get dimensions of the background the sprite messed up
        # calculate clean rect

#        dirtyrect = bg2.subsurface((abs(self.f_x - self.f_w//2), abs(self.f_y - self.f_h//2), abs(self.f_w*2), abs(self.f_h*2)))  # old
        dirtyrect = bg2.subsurface(self.fish_main_rect)

        # we need to do some editions to the fish rect when calculating the dirty rect around 
        # this is to ensure that no traces of the fish get eft on
        # and then we blit it on before the sprite
#        self.screen.blit(dirtyrect, (self.fish_main_rect.topleft[0], self.fish_main_rect.topleft[1]))
        # blit clean rect on top of "dirty" screen

        for fishes in cpu_fishes.sprites():
            if (self.fish_main_rect.colliderect(fishes.fish_main_rect)):
#                rl.remove(fishes.fish_main_rect) # remove that #no need to remove !!!
#                rl.remove(self.fish_main_rect) # no need to remove

                a = self.screen.blit(fishes.fish_main_surf[fishes.fish_frame_num], fishes.fish_main_rect.topleft)
                b = self.screen.blit(self.fish_main_surf[self.fish_frame_num], self.fish_main_rect.topleft)

                rl.append(a)
                rl.append(b)
                print("done magic")

        self.fish_main_rect = self.screen.blit(self.fish_main_surf[self.fish_frame_num], self.fish_main_rect.topleft) #update pos of fis
        rl.append(self.fish_main_rect)

    def keys_pressed(self, k):
        #this is to handle all movements
        #when the user is holding a certain key down
        if k[K_RIGHT]:
            f.update(1)
        if k[K_LEFT]:
            f.update(2)
        if k[K_UP]:
            f.update(3)
        if k[K_DOWN]:
            f.update(4)


rl = []

bg_file = 'fishdish/fishtitle.png' # for starting screen background
background = pygame.image.load(bg_file)

#load up main surface with the height and width of the starting background image
screen = pygame.display.set_mode([background.get_width(), background.get_height()], 0 , 32)

main_bg_file = 'fishdish/fishtitle.png' # for game screen background
main_bg = pygame.image.load(main_bg_file)

pygame.init()
windowSize = [background.get_width(), background.get_height()]

pygame.display.set_caption("FISH GAME")

#cpu fishes group
cpu_fishes = pygame.sprite.Group()
main_fish = pygame.sprite.Group()
#cpu_fishes = pygame.sprite.RenderUpdates()
#main_fish = pygame.sprite.RenderUpdates()


#initialize f as an instance of the main fish class
f = Fish(screen, '6main_fish')
available_sprites = ['yellow_fish','blue_fish']
cpu_f1 = cpu_Fish(screen, 'yellow_fish', right, 10, 0, 25)
cpu_f2 = cpu_Fish(screen, 'blue_fish', right, 10, 0, 200)
cpu_f3 = cpu_Fish(screen, 'blue_fish', right, 10,0,200)

cpu_fishes.add(cpu_f1)
cpu_fishes.add(cpu_f2)
cpu_fishes.add(cpu_f3)
#add f fish to the main_fish sprite group
main_fish.add(f)

start_screen = True
game = False
            
clock = pygame.time.Clock()

while True:
    if start_screen:
        #display the starting screen background
        screen.blit(background,(0,0))
        pygame.display.update()
        main_bg_off = True

    if game:
        if main_bg_off:
            screen.blit(main_bg,(0,0))
            main_bg_off = False
        f.keys_pressed(pygame.key.get_pressed())

    for event in pygame.event.get():
        
        #main game loop 
        # interesting stuff happens here

        if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == K_SPACE):
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == K_RIGHT:
            f.fish_direction = right
            f.update(1)
        if event.type == pygame.KEYDOWN and event.key == K_LEFT:
            f.fish_direction = left
            f.update(2)
        if event.type == pygame.KEYDOWN and event.key == K_UP:
            f.update(3)
        if event.type == pygame.KEYDOWN and event.key == K_DOWN:
            f.update(4)


        if (event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN) and start_screen):
            #pressed enter
            #switch to game mode
            game = True
            start_screen = False
            
            
    clock.tick(30)

    if game:
        #so we only update when we are past the starting screen 
        #otherwise we update for no reason
        cpu_fishes.update()
        main_fish.update()
        cpulist = cpu_fishes.sprites()
        for fish in cpulist:
            if fish.get_f_y() > 300:
                cpu_fishes.remove(fish)
                cpu_fishes.add(add_a_new_cpu(screen, available_sprites))
            elif fish.get_f_y() < -60:
                cpu_fishes.remove(fish)
                cpu_fishes.add(add_a_new_cpu(screen, available_sprites))
            if fish.get_f_x() > 470:
                cpu_fishes.remove(fish)
                cpu_fishes.add(add_a_new_cpu(screen, available_sprites))
            elif fish.get_f_x() < -60:
                cpu_fishes.remove(fish)
                cpu_fishes.add(add_a_new_cpu(screen, available_sprites))
#        print(rl)
        pygame.display.update(rl)
        rl = []



        

        
