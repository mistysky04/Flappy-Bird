import pygame
from sys import exit
import random

#Constant variables
pipe_distance = 720
speed = 5

#Classes & Functions
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        bird_1 = pygame.image.load('desktop/Pygamefiles/Flappy Bird/Graphics/Bird/Bird 4.png').convert_alpha()
        bird_1 = pygame.transform.scale(bird_1, (70, 30))

        bird_2 = pygame.image.load('desktop/Pygamefiles/Flappy Bird/Graphics/Bird/Bird 5.png').convert_alpha()
        bird_2 = pygame.transform.scale(bird_2, (70, 30))
        #Place images in list for animation + set index to swap between 2 images
        #"self" is used whenever we want to access variables throughout a class (not just in init method)
        self.frames = [bird_1, bird_2]
        self.bird_index = 0
        
        self.image = self.frames[self.bird_index]
        self.rect = self.image.get_rect(center = (50,300))
        self.gravity = 0
    
    def player_input(self):
        #Gives all inputs for keys pressed 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            #How high each button press will cause the bird to "jump" 
            #larger (-) value = jumps higher 
            #DO NOT make it +=, it will cause the bird to move REALLY WACK
            self.gravity = -4.5
    
    def apply_gravity(self):
        #How fast player falls (i.e. we want them to fall slightly slower for easier gameplay)
        self.gravity += 0.7
        self.rect.y += self.gravity
        if self.rect.bottom >= 580:
            self.rect.bottom = 580
    
    def animation(self):
        self.bird_index += 0.1
        if self.bird_index >= len(self.frames): self.bird_index = 0
        self.image = self.frames[int(self.bird_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

class PipeDown(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        pipe_down = pygame.image.load('desktop/Pygamefiles/Flappy Bird/Graphics/Pipes/Pipe_2_sprite.png').convert_alpha()
        self.image = pipe_down

        global down_y_pos
        down_y_pos= random.randint(-550, -150)
        self.rect = self.image.get_rect(midtop = (1150, down_y_pos))

    def update(self):
        #Speed of pipe movement
        self.rect.x -= speed
        self.destroy()

    def destroy(self):
        #Destroy pipes once they move too far off screen 
        if self.rect.x <= -100:
            self.kill()

class PipeUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pipe_up = pygame.image.load('desktop/Pygamefiles/Flappy Bird/Graphics/Pipes/Pipe_1_sprite.png').convert_alpha()
        self.image = pipe_up
        up_y_pos = down_y_pos + pipe_distance
        self.rect = self.image.get_rect(midtop = (1150, up_y_pos))

    def update(self):
        #Speed of pipe movement
        self.rect.x -= speed
        self.destroy()

    def destroy(self):
        #Destroy pipes once they move too far off screen 
        if self.rect.x <= -100:
            self.kill()

#def display_score():

def sprite_collisions():
    if pygame.sprite.spritecollide(bird.sprite, pipe_down, False) or pygame.sprite.spritecollide(bird.sprite, pipe_up, False):
        pipe_down.empty()
        pipe_up.empty()
        return False
    else: return True
        

#General startup

#Initialize pygame settings
pygame.init()
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
test_font = pygame.font.Font('desktop/Pygamefiles/PygameIntro/font/Pixeltype.ttf', 50)

#Set game state
game_active = False
start_time = 0
score = 0

#Import music 

#Groups --> These are your ACTUAL SPRITES
#Use Group() when you want to have multiple of the same sprite on the screen
#GroupSingle() used when only 1 of that sprite will be on the screen at a time
pipe_down = pygame.sprite.Group()
pipe_up = pygame.sprite.Group()

bird = pygame.sprite.GroupSingle()
#Add instance of player group i.e. bird 
bird.add(Player())


#Create game background & convert alpha lock to erase transparent box 
sky_surf = pygame.image.load('desktop/Pygamefiles/Flappy Bird/Graphics/Background/Background_SimpleSky.png').convert_alpha()
ground_surf = pygame.image.load('desktop/Pygamefiles/Flappy Bird/Graphics/Foreground/Ground_Smaller.png').convert_alpha()

#Timer
#Must add +1 since we already have an event as the main game (?) note* please rewatch this part of the video
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


#While game is running
while True:
    #For ALL events in game
    for event in pygame.event.get():
        #Game ends if player clicks 'x' 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #Add obstacles to group
        if game_active:
            if event.type == obstacle_timer:
                pipe_down.add(PipeDown())
                pipe_up.add(PipeUp())
        else:
            #If you press the enter key down, the game will start
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
        #Keyboard/mouse functionality
    #ONLY when game is ACTIVE
    if game_active:
        #Place background on screen
        screen.blit(sky_surf,(0,0))
        
        #draw obstacles on screen
        #Spritegroup main function = draw + update all sprites
        pipe_down.draw(screen)
        pipe_down.update()

        pipe_up.draw(screen)
        pipe_up.update()

        bird.draw(screen)
        bird.update()

        #Place foreground in front of pipes
        screen.blit(ground_surf,(0,460))
        
        #If game_active = true, include sprite_collisions
        game_active = sprite_collisions()
    else: 
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,460))
        
    #Update screen with components of active game 
    pygame.display.update()
    clock.tick(60)