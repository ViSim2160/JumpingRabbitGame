import pygame
import os
import random
import sys
pygame.init()

SCREEN_HEIGHT = 600 
SCREEN_WIDTH = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Bunny", "RabbitRun1.png")),
           pygame.image.load(os.path.join("Assets/Bunny", "RabbitRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Bunny", "RabbitJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Bunny", "RabbitDuck1.png")),
           pygame.image.load(os.path.join("Assets/Bunny", "RabbitDuck2.png"))]

SMALL_CARROT = [pygame.image.load(os.path.join("Assets/Carrots", "SmallCarrot1.png")),
                pygame.image.load(os.path.join("Assets/Carrots", "SmallCarrot2.png")),
                pygame.image.load(os.path.join("Assets/Carrots", "SmallCarrot3.png"))]
LARGE_CARROT = [pygame.image.load(os.path.join("Assets/Carrots", "LargeCarrot1.png")),
                pygame.image.load(os.path.join("Assets/Carrots", "LargeCarrot2.png")),
                pygame.image.load(os.path.join("Assets/Carrots", "LargeCarrot3.png"))]

BEE = [pygame.image.load(os.path.join("Assets/Bee", "Bee1.png")),
        pygame.image.load(os.path.join("Assets/Bee", "Bee2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

CLOUD_1 = pygame.image.load(os.path.join("Assets/Other", "Cloud1.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

START_RABBIT = pygame.image.load(os.path.join("Assets/Other", "StartRabbit.png"))
DEATH_RABBIT = pygame.image.load(os.path.join("Assets/Other", "DeathRabbit.png"))

NAME_GAME = pygame.image.load(os.path.join("Assets/Other", "JumpingRabbit.png"))
ANY_KEY = pygame.image.load(os.path.join("Assets/Other", "PressAnyKey.png"))
GAME_OVER = pygame.image.load(os.path.join("Assets/Other", "GameOver.png"))


class Jumpingrabbit:
    X_POS = 300
    Y_POS = 235
    Y_POS_DUCK = 253 
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.rabbit_duck = False
        self.rabbit_run = True
        self.rabbit_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.rabbit_rect = self.image.get_rect()
        self.rabbit_rect.x = self.X_POS
        self.rabbit_rect.y = self.Y_POS

    def update(self, userInput):
        if self.rabbit_duck:
            self.duck()
        if self.rabbit_run:
            self.run()
        if self.rabbit_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.rabbit_jump:
            self.rabbit_duck = False
            self.rabbit_run = False
            self.rabbit_jump = True
        elif userInput[pygame.K_DOWN] and not self.rabbit_jump:
            self.rabbit_duck = True
            self.rabbit_run = False
            self.rabbit_jump = False
        elif not (self.rabbit_jump or userInput[pygame.K_DOWN]):
            self.rabbit_duck = False
            self.rabbit_run = True
            self.rabbit_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.rabbit_rect = self.image.get_rect()
        self.rabbit_rect.x = self.X_POS
        self.rabbit_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.rabbit_rect = self.image.get_rect()
        self.rabbit_rect.x = self.X_POS
        self.rabbit_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.rabbit_jump:
            self.rabbit_rect.y -= self.jump_vel * 5
            self.jump_vel -= 1
        if self.jump_vel < - self.JUMP_VEL:
            self.rabbit_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rabbit_rect.x, self.rabbit_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(0,100)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(500, 1000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Cloud1:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(0,400)
        self.y = random.randint(50, 100)
        self.image = CLOUD_1
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(100, 500)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))
        
        
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCarrot(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 245


class LargeCarrot(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 235


class Bee(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 130
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Jumpingrabbit()
    cloud = Cloud()
    cloud1 = Cloud1()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 300
    points = 0
    font = pygame.font.Font('Grand9K Pixel.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 200 == 0:
            game_speed += 1

        text = font.render("SCORE: " + str(points), True, (58, 62, 97))
        textRect = text.get_rect()
        textRect.center = (700, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((23, 165, 212))
        userInput = pygame.key.get_pressed()

        background()
        
        cloud.draw(SCREEN)
        cloud.update()
 
        cloud1.draw(SCREEN)
        cloud1.update()
 
        
        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCarrot(SMALL_CARROT))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCarrot(LARGE_CARROT))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bee(BEE))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.rabbit_rect.colliderect(obstacle.rect):
                pygame.time.delay(1500)
                death_count += 1
                menu(death_count)
       
        
        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((58, 62, 97))
        font = pygame.font.Font('Grand9K Pixel.ttf', 20)

        if death_count == 0:
            
            SCREEN.blit(START_RABBIT, (SCREEN_WIDTH // 2 - 55, SCREEN_HEIGHT // 2 - 140))
            SCREEN.blit(NAME_GAME, (SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2 - 20))
            SCREEN.blit(ANY_KEY, (SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2 + 30))
            
            
        elif death_count > 0:
            text = font.render("PRESS ANY KEY TO RESTART", True, (249, 179, 220))
            score = font.render("current score:  " + str(points) + " points", True, (249, 179, 220))
            scoreRect = score.get_rect()
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
            SCREEN.blit(text, textRect)
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
            SCREEN.blit(DEATH_RABBIT, (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
            SCREEN.blit(GAME_OVER, (SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2 - 40))
            SCREEN.blit(score, scoreRect)
        
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)