import pygame
from sys import exit
import random

#CONSTANT VARIABLES
pipe_distance = 720
speed = 5
gravity = 0

#CLASSES
class Player(pygame.sprite.Sprite):
    def __init__(self):
        #Inherit properties of sprite class
        super().__init__()
        #Import bird pictures & scale
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
        self.gravity = gravity
    
    def player_input(self):
        #Gives all inputs for keys pressed 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            #How high each button press will cause the bird to "jump" 
            #larger (-) value = jumps higher 
            #DO NOT make it +=, it will cause the bird to move REALLY WACK
            self.gravity = -5.5
    
    def apply_gravity(self):
        #How fast player falls (i.e. we want them to fall slightly slower for easier gameplay)
        self.gravity += 0.7
        self.rect.y += self.gravity
        #Ensure player does not go beyond screen bounds
        if self.rect.bottom >= 580:
            self.rect.bottom = 580
    
    def animation(self):
        #Set animation rate & loop between images
        self.bird_index += 0.1
        if self.bird_index >= len(self.frames): self.bird_index = 0
        self.image = self.frames[int(self.bird_index)]
    
    def update(self):
        #Continuously update all functions for smooth gameplay
        self.player_input()
        self.apply_gravity()
        self.animation()

class PipeDown(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #Import images
        pipe_down = pygame.image.load('desktop/Pygamefiles/Flappy Bird/Graphics/Pipes/Pipe_2_sprite.png').convert_alpha()
        self.image = pipe_down

        #Randomly set y-value of pipe
        global down_y_pos
        down_y_pos= random.randint(-550, -150)
        self.rect = self.image.get_rect(midtop = (1150, down_y_pos))

    def update(self):
        #Speed of pipe movement (in Update b/c pipe must continuously move across screen)
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

        #Y position of pipe based on chosen Y position of downward pipe + pipe distance value (to create space b/w pipes)
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

class ScoreCounter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #Create line to sit in empty space b/w two pipes to detect if player avoids hitting pipe = score increases
        line = pygame.image.load('desktop/Pygamefiles/Flappy Bird/Graphics/Line.png').convert_alpha()
        self.image = line
        self.rect = self.image.get_rect(midtop = (1150, 0))
        
    def update(self):
        #Speed of line equal to speed of pipes so they move together
        self.rect.x -= speed
        self.destroy()

    def destroy(self):
        #Destroy line once moved off screen
        if self.rect.x <= -100:
            self.kill()

#Functions
def display_score():
    score = 0
    #Collisions between player & score counter line
    #Line will disappear after collision to ensure score only increases by ONE
    collisions = pygame.sprite.spritecollide(bird.sprite, score_counter, True)
    if collisions:
        score += 1
    #Set up score display on screen
    score_surf = score_font.render(f'Score {score_display}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (500,50))
    screen.blit(score_surf,score_rect)
    return score
    
def sprite_collisions():
    #If player collides with pipes, game stops
    if pygame.sprite.spritecollide(bird.sprite, pipe_down, False) or pygame.sprite.spritecollide(bird.sprite, pipe_up, False):
        #Empty all groups before game restarts so pipes & score counter respawn from right side of screen
        pipe_down.empty()
        pipe_up.empty()
        score_counter.empty()
        
        #Use return statements to change boolean of game_state
        #Game_active = false once collision happens i.e. game will END 
        return False
    #If player hits ground, game stops
    elif bird.sprite.rect.bottom == 580:
        pipe_down.empty()
        pipe_up.empty()
        score_counter.empty()
        return False
    else: 
        return True
        
#INITIALIZE PYGAME SETTINGS
pygame.init()

#screen size + screen name
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption('Flappy Bird')

#Clock sets framerate of gameplay
clock = pygame.time.Clock()

#fonts
score_font = pygame.font.Font('desktop/Pygamefiles/Flappy Bird/Fonts/arcadeclassic/ARCADECLASSIC.TTF', 50)
instruct_font = pygame.font.Font('desktop/Pygamefiles/Flappy Bird/Fonts/arcadeclassic/ARCADECLASSIC.TTF', 40)

#GAME STATES
game_active = False
score_display = 0

#MUSIC

#GROUPS

#Groups contain Sprites i.e. can be called without specifying .sprite
#Use Group() when you want MULTIPLE of a single sprite on the screen at a time
pipe_down = pygame.sprite.Group()
pipe_up = pygame.sprite.Group()
score_counter = pygame.sprite.Group()

#GroupSingle only contains a single sprite BUT must be called with .sprite as a result
#Use GroupSingle() when you only want ONE single sprite on screen at a time e.g. player character
bird = pygame.sprite.GroupSingle()
#Add instance of player group i.e. bird 
bird.add(Player())


#IMPORT IMAGES

#Background/foreground
#Convert alpha erases transparent box around png images
sky_surf = pygame.image.load('desktop/Pygamefiles/Flappy Bird/Graphics/Background/Background_SimpleSky.png').convert_alpha()
ground_surf = pygame.image.load('desktop/Pygamefiles/Flappy Bird/Graphics/Foreground/Ground_Smaller.png').convert_alpha()

#Score message
score_surf = score_font.render(f'Score {score_display}', False,(64,64,64))
score_rect = score_surf.get_rect(midtop = (500,50))

#Logo and Bird for start screen
logo_surf = pygame.image.load('desktop/Pygamefiles/Flappy Bird/Graphics/Logo Sprite.png').convert_alpha()
bird_surf = pygame.image.load('desktop/Pygamefiles/Flappy Bird/Graphics/Bird/Bird 4.png').convert_alpha()

#TIMERS
#create specific event for intervals of obstacles to appear on screen
#set_timer specifies how often we want each obstacles to appear (via milliseconds)
obstacle_timer = pygame.USEREVENT
pygame.time.set_timer(obstacle_timer, 1500)


#GAME LOOP
while True:
    #For ALL events in game
    for event in pygame.event.get():
        #Game ends if player clicks 'x' 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            #Initialize obstacles into each group
            if event.type == obstacle_timer:
                pipe_down.add(PipeDown())
                pipe_up.add(PipeUp())
                score_counter.add(ScoreCounter())
        else:
            #If you press the enter key down, the game will start
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                game_active = True
                #Reset score to 0
                score_display = 0
                #Bird starts at same spot on screen each time game restarts
                #Gravity reset to 0
                bird.sprite.rect.x = 50
                bird.sprite.rect.y = 300
                bird.sprite.gravity = 0
    if game_active:
        #Line for score tracking behind EVERYTHING else (dont want player to see)
        score_counter.draw(screen)
        score_counter.update()   

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
        
        #If sprite collision occurs, we will return False and game will end
        game_active = sprite_collisions()

        #Score will update on screen
        score_display += display_score()
    
    else: 
        #Set up main menu screen
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,460))
        screen.blit(logo_surf, (150,30))
        screen.blit(bird_surf, (470,350))

        #If player gets score 0 OR player just starts playing
        #Display instructions
        if score_display == 0:
            instruct_surf = instruct_font.render(f'Press Up Key to Start', False, (64,64,64))
            instruct_rect = instruct_surf.get_rect(midtop = (500, 450))
            screen.blit(instruct_surf, instruct_rect)

            instruct2_surf = instruct_font.render(f'Use Arrow Keys to Move', False, (64,64,64))
            instruct2_rect = instruct2_surf.get_rect(midtop = (500, 500))
            screen.blit(instruct2_surf, instruct2_rect)
        #If player finishes round of game
        #Display their score 
        else:
            score_surf = score_font.render(f'Score {score_display}', False,(64,64,64))
            score_rect = score_surf.get_rect(midtop = (500,500))
            screen.blit(score_surf, score_rect)
    #Update screen with components of active game 
    pygame.display.update()
    #Game framerate
    clock.tick(60)