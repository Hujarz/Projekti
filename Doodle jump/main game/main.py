import pygame
import random
import os
from Spritesheet import SpriteSheet
from enemy import Enemy
from pygame import mixer

mixer.init()
pygame.init()

#game window
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Lēcējs')

#frame rate
clock = pygame.time.Clock()
FPS = 60

#load music and sounds
jump_fx = pygame.mixer.Sound('assets/assets_jump.mp3')
jump_fx.set_volume(0.1)
death_fx = pygame.mixer.Sound('assets/assets_death.mp3')
death_fx.set_volume(0.1)

#game variables
SCROLL_THRESH = 200
GRAVITY = 1
MAX_PLATFORMS = 15
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0
if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0



#def colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (105,143,158)
#define font
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 20)


#load images
background = pygame.image.load('assets/bacg.png').convert_alpha()
jumpy_image = pygame.image.load('assets/player_idle.png').convert_alpha()
platform_image = pygame.image.load('assets/platform.png').convert_alpha()

#bird spritsheet
bird_sheet_img = pygame.image.load('assets/bird.png').convert_alpha()
bird_sheet = SpriteSheet(bird_sheet_img)

#function for ouputting text on the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#drawing info panel
def draw_panel():
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(screen, BLACK, (0, 30), (SCREEN_WIDTH, 30), 2)
    draw_text('SCORE: ' + str(score), font_small, BLACK, 0, 0)


#draw the bacground
def draw_bg(bg_scroll):
    screen.blit(background, (0, 0 + bg_scroll))
    screen.blit(background, (0, -600 + bg_scroll))

#player class
class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(jumpy_image, (40, 55))
        self.width = 28
        self.height = 50
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        #reset variables
        dx = 0
        dy = 0
        scroll = 0

        #key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx = -10
            self.flip = True
        if key[pygame.K_RIGHT]:
            dx = 10
            self.flip = False

        #gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #ensure player dont go off the edge
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right


        #check collision with platforms
        for platform in platform_group:
            #collision in y pos
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20
                        jump_fx.play()
        

        #check if the player has bounced to the top
        if self.rect.top <= SCROLL_THRESH:
            #if player is jumping
            if self.vel_y <0:
                scroll = -dy



        #update rect pos
        self.rect.x += dx
        self.rect.y += dy + scroll

        #update mask
        self.mask = pygame.mask.from_surface(self.image)

        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 6, self.rect.y - 5))
        #pygame.draw.rect(screen, WHITE, self.rect, 2)

#platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 5)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        #move platform side to side if it is suppose to
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        #change platform direction if side or moved fully
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0
        
        #update platform vertical pos
        self.rect.y += scroll

        #chack if platform has gone off the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


    

#palyer instance
jumpy = Player(SCREEN_WIDTH // 2 , SCREEN_HEIGHT - 150)

#create sprite group
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

#create starting platform
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
platform_group.add(platform)



run = True
while run:

    clock.tick(FPS)


    if game_over == False:
        scroll = jumpy.move()
        
        #draw background
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        #generate platforms
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            p_type = random.randint(1, 2)
            if p_type == 1 and score > 750:
                p_moving = True
            else: 
                p_moving = False
            platform = Platform(p_x, p_y, p_w, p_moving)
            platform_group.add(platform) 


        #update platforms
        platform_group.update(scroll)

        #generate enemies
        if len(enemy_group) == 0 and score > 3000:
            enemy = Enemy(SCREEN_WIDTH, 100, bird_sheet, 1.5)
            enemy_group.add(enemy)


        #update enemies
        enemy_group.update(scroll, SCREEN_WIDTH)


        #update score
        if scroll > 0:
            score += scroll

        #draw line at the high score
        pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESH), (SCREEN_WIDTH, score - high_score + SCROLL_THRESH), 3)
        draw_text('High Score', font_small, WHITE, SCREEN_WIDTH - 130, score - high_score + SCROLL_THRESH)

        #draw sprites
        platform_group.draw(screen)
        enemy_group.draw(screen)
        jumpy.draw()

        #draw panel
        draw_panel()

        #check game over
        if jumpy.rect.top > SCREEN_HEIGHT:
            death_fx.play()
            game_over = True
            
        #check collision with enemy
        if pygame.sprite.spritecollide(jumpy, enemy_group, False):

            if pygame.sprite.spritecollide(jumpy, enemy_group, False, pygame.sprite.collide_mask):
                game_over = True
                death_fx.play()
        
    else:
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 10
            for y in range(0, 60, 2):
                pygame.draw.rect(screen, BLACK, (0, y * 10, fade_counter, 10))
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (y + 1) * 10, SCREEN_WIDTH, 10))
        else:
            draw_text('Game Over!', font_big, WHITE, 150, 200)
            draw_text('Score: ' + str(score), font_big, WHITE, 160, 250)
            draw_text('Press space to play again', font_big, WHITE, 80, 300)

            #update high_score
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                #reset variables
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                #reposition jumpy
                jumpy.rect.center = (SCREEN_WIDTH // 2 , SCREEN_HEIGHT - 150)

                #reset enemies
                enemy_group.empty()

                #reset platforms
                platform_group.empty()
                #create starting platform
                platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
                platform_group.add(platform)

    #handle event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            run = False


    pygame.display.update()

pygame.quit()