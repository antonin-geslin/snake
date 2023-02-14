import pygame
from pygame.locals import *
import random
import os
import json
from enum import Enum


#Gestion des score et du fichier json#
def write_scores(joueur, score):
    entry = {
                'Joueur' : str(joueur),
                'Score' : score,
            }
    with open('score.json', 'r') as file:
        data = json.load(file)

    data.append(entry)

    with open('score.json', 'w') as file:
        json.dump(data, file)

def read_scores():
    with open('score.json', 'r') as file:
        json_object = json.load(file)
    json_object.sort(key=lambda x: x["Score"], reverse = True)
    y_offset = 0
    for score in json_object:
        textsurface = pygame.font.Font(None, 40).render(str(score['Score']), False, (5, 21, 5))
        window.blit(textsurface, (540, 200 + y_offset))
        y_offset += 40

    y_offset = 0
    for joueur in json_object:
        textsurface = pygame.font.Font(None, 40).render(str(joueur['Joueur']), False, (5, 21, 5))
        window.blit(textsurface, (200, 200 + y_offset))
        y_offset += 40

#Gestion des score et du fichier json#

#Affichage du menu et redirections#
def display_menu():
    global menu
    global score_menu
    global game
    global color
    window.fill(color)
    title = pygame.font.Font(None, 60).render("SNAKE", True, (5,21,5))
    window.blit(title, (320, 50))
    play = pygame.font.Font(None, 50).render("Play", True, (5,21,5))
    play_rect = play.get_rect(topleft=(360, 300))
    window.blit(play, play_rect)
    scores = pygame.font.Font(None, 50).render("Scores", True, (5,21,5))
    scores_rect = scores.get_rect(topleft=(340, 360))
    window.blit(scores, scores_rect)
    x,y=pygame.mouse.get_pos()
    pygame.display.update()
    if play_rect.collidepoint(x,y):
        if pygame.mouse.get_pressed() == (1,0,0):
            menu = 0
            game = 1
    if scores_rect.collidepoint(x, y):
        if pygame.mouse.get_pressed() == (1,0,0):
            menu = 0
            score_menu = 1
    pygame.display.update()

#Affichage du menu et redirections#


#Affichage de l'écran de jeu
def display_game():
    global color
    global score
    window.fill(color)
    counter = pygame.font.Font(None, 50).render("Score : "  + str(score), True, (5,21,5))
    counter_rect = counter.get_rect(topright=(750, 30))
    window.blit(counter, counter_rect)
    pygame.display.update()

#Affichage de l'écran de jeu

#Affichage de la fenetre de score# 
def display_score():
    global color
    global menu
    global score_menu
    window.fill(color)
    title = pygame.font.Font(None, 50).render("HIGH SCORES", True, (5,21,5))
    title_rect = title.get_rect(topleft=(290, 50))
    window.blit(title, title_rect)
    scores = pygame.font.Font(None, 50).render("Scores", True, (5,21,5))
    scores_rect = scores.get_rect(topleft=(500, 150))
    window.blit(scores, scores_rect)
    joueur = pygame.font.Font(None, 50).render("Joueur", True, (5,21,5))
    joueur_rect = joueur.get_rect(topleft=(200, 150))
    window.blit(joueur, joueur_rect)
    read_scores()
    menu = pygame.font.Font(None, 50).render("Return to menu", True, (5,21,5))
    menu_rect = menu.get_rect(topleft=(280, 700))
    window.blit(menu, menu_rect)
    x,y=pygame.mouse.get_pos()
    if menu_rect.collidepoint(x,y):
        if pygame.mouse.get_pressed() == (1,0,0):
            menu = 1
            score_menu = 0
    pygame.display.update()

#Affichage de la fenetre de score# 


#Classe snake#
class Direction(Enum):
  UP = 0
  DOWN = 1
  LEFT = 2
  RIGHT = 3

class Snake:
    length = None
    direction = None
    body = None
    block_size = None
    color = (65,104,66)
    bounds = None

    def __init__(self, block_size, bounds):
        self.block_size = block_size
        self.bounds = bounds
        self.respawn()

    def respawn(self):
        self.length = 3
        self.body = [(20,20),(20,40),(20,60)]
        self.direction = Direction.DOWN

    def draw(self, window):
        for segment in self.body:
            pygame.draw.rect(window, self.color, (segment[0],segment[1],self.block_size, self.block_size))

    def move(self):
        curr_head = self.body[-1]
        if self.direction == Direction.DOWN:
            next_head = (curr_head[0], curr_head[1] + self.block_size)
            self.body.append(next_head)
        elif self.direction == Direction.UP:
            next_head = (curr_head[0], curr_head[1] - self.block_size)
            self.body.append(next_head)
        elif self.direction == Direction.RIGHT:
            next_head = (curr_head[0] + self.block_size, curr_head[1])
            self.body.append(next_head)
        elif self.direction == Direction.LEFT:
            next_head = (curr_head[0] - self.block_size, curr_head[1])
            self.body.append(next_head)

        if self.length < len(self.body):
            self.body.pop(0)

    def check_move(self, direction):
        if self.direction == Direction.DOWN and direction != Direction.UP:
            self.direction = direction
        elif self.direction == Direction.UP and direction != Direction.DOWN:
            self.direction = direction
        elif self.direction == Direction.LEFT and direction != Direction.RIGHT:
            self.direction = direction
        elif self.direction == Direction.RIGHT and direction != Direction.LEFT:
            self.direction = direction

    def eat(self):
        global score
        self.length += 1
        score += 1

    def check_food(self, food):
        head = self.body[-1]
        if head[0] == food.x and head[1] == food.y:
            self.eat()
            food.respawn()

    def eat_tail(self):
        head = self.body[-1]
        for i in range(len(self.body) - 1):
            segment = self.body[i]
            if head[0] == segment[0] and head[1] == segment[1]:
                return(True)

    def check_bounds(self):
        head = self.body[-1]
        if head[0] < 0:
            return True
        elif head[0] >= self.bounds[0]:
            return(True)
        elif head[1] < 0:
            return(True)
        elif head[1] >= self.bounds[1]:
            return(True)
#Classe snake#



#Classe food#
class Food:
    block_size = None
    color = (255,0,0)
    x = None
    y = None
    bounds = None

    def __init__(self, block_size, bounds):
        self.block_size = block_size
        self.bounds = bounds
        self.respawn()

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.block_size, self.block_size))

    def respawn(self):
        blocks_in_x = (self.bounds[0])/self.block_size; 
        blocks_in_y = (self.bounds[1])/self.block_size; 
        self.x = random.randint(0, blocks_in_x - 1) * self.block_size
        self.y = random.randint(0, blocks_in_y - 1) * self.block_size
#Classe food#

#Gestion du game over et redirections#
def game_over(snake):
    global joueur
    global score
    global game
    global over
    if snake.eat_tail():
        write_scores(joueur, score)
        game = 0
        over = 1
    elif snake.check_bounds():
        write_scores(joueur, score)
        game = 0
        over = 1
    pygame.display.update()
#Gestion du game over et redirections#


joueur = input("PLAYER NAME : ")

#initialisation de la fenetre de jeu
pygame.init()
bounds = (800,800)
window = pygame.display.set_mode(bounds)
#initialisation de la fenetre de jeu

#déclaration de variables gobales
color = (153,202,151)
block_size = 20
snake = Snake(block_size, bounds)
food = Food(block_size, bounds)
running = True
menu = 1
game = 0
over = 0
score_menu = 0
score = 0
x,y = pygame.mouse.get_pos()
#déclaration de variables gobales

#Boucle de jeu#
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    while menu == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        display_menu()
    while game == 1:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game = 0
        display_game()
        snake.draw(window)
        food.draw(window)
        snake.move()
        snake.check_food(food)
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            snake.check_move(Direction.LEFT)
        elif keys[pygame.K_RIGHT]:
            snake.check_move(Direction.RIGHT)
        elif keys[pygame.K_UP]:
            snake.check_move(Direction.UP)
        elif keys[pygame.K_DOWN]:
            snake.check_move(Direction.DOWN)
        game_over(snake)
        pygame.display.update()
    while score_menu == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                score_menu = 0
        display_score()
        pygame.display.update()
    while over == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                over = 0
        over_ = pygame.font.Font(None, 50).render("GAME OVER", True, (5,21,5))
        over_rect = over_.get_rect(topleft=(300, 400))
        window.blit(over_, over_rect)
        menu2 = pygame.font.Font(None, 50).render("Return to menu", True, (5,21,5))
        menu2_rect = menu2.get_rect(topleft=(280, 700))
        window.blit(menu2, menu2_rect)
        quit = pygame.font.Font(None, 50).render("Quit", True, (5,21,5))
        quit_rect = quit.get_rect(topleft=(380, 750))
        window.blit(quit, quit_rect)
        pygame.display.update()
        x,y=pygame.mouse.get_pos()
        if menu2_rect.collidepoint(x,y):
            if pygame.mouse.get_pressed() == (1,0,0):
                menu = 1
                over = 0
                color = (153,202,151)
                block_size = 20
                snake = Snake(block_size, bounds)
                food = Food(block_size, bounds)
                running = True
                menu = 1
                game = 0
                over = 0
                score_menu = 0
                score = 0
                x,y = pygame.mouse.get_pos()
        if quit_rect.collidepoint(x,y):
            if pygame.mouse.get_pressed() == (1,0,0):
                running = False
pygame.quit()
exit()


#Boucle de jeu#