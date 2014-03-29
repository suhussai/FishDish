#drawing going to be done in 3 three 
import pygame
import random

right = 'right'
left = 'left'

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



class Creep(pygame.sprite.Sprite):
    
    def __init__(self,screen,  fish_name, windowSize, main_bg_file, fish_speed = 10, x = 200, y = 200, fish_width = 0, fish_height = 0 ):


        #initialze important variables
        #screen so we can blit in our class
        #onto the main screen
        self.screen = screen
        self.windowSize = windowSize
        self.main_bg_file = main_bg_file
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
        self.fish_main_rect2 = self.fish_main_surf[0].get_rect()

    def updatecreep(self, direction_of_movement = 0):
        # direction == 0 no movement
        # direction == 1 right
        # direction == 2 left
        # direction == 3 up
        # direction == 4 down


        d = direction_of_movement
        if d == 1:
            self.f_x += self.f_s
        elif d == 2:
            self.f_x -= self.f_s
        elif d == 3:
            self.f_y -= self.f_s
        elif d == 4:
            self.f_y += self.f_s


        self.f_x = squeeze(self.f_x, self.windowSize[0] - self.f_w*2, self.f_w)
        self.f_y = squeeze(self.f_y, self.windowSize[1] - self.f_h*2, self.f_h)
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

        bg2 = pygame.image.load(self.main_bg_file)
#        bg2.fill((255,0,0)) #fills dirty with red to color to show how large rect is 
        #dirty rect calc to get dimensions of the background the sprite messed up
        # calculate clean rect
        dirtyrect = bg2.subsurface((abs(self.f_x - self.f_w//2), abs(self.f_y - self.f_h//2), abs(self.f_w*2), abs(self.f_h*2))) 

        # we need to do some editions to the fish rect when calculating the dirty rect around 
        # this is to ensure that no traces of the fish get eft on
        # and then we blit it on before the sprite
        self.screen.blit(dirtyrect, (self.fish_main_rect.topleft[0] - self.f_w//2, self.fish_main_rect.topleft[1] - self.f_h//2))
        # blit clean rect on top of "dirty" screen

        self.screen.blit(self.fish_main_surf[self.fish_frame_num], self.fish_main_rect.topleft) #update pos of fish
