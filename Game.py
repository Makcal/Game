import os
import pygame
from time import sleep as delay
from random import randint

def left(n):
    print('|', end = '')
    for i in range(n):
        print(' ', end = '')

def right(n):
    for i in range(n):
        print(' ', end = '')
    print('|')

def full():
    global FIELD_LENGTH, START_BR_LENGTH
    left(0)
    right(FIELD_LENGTH)

def shift():
    global pos, direction, brick_length, START_BR_LENGTH, FIELD_LENGTH
    pos += 1 * direction
    if (pos - 1 + brick_length == FIELD_LENGTH and direction == 1) or (pos == 1 and direction == -1):
        direction *= -1

def brick(n):
    global BRICK_SYMB
    for i in range(n):
        print(BRICK_SYMB, end = '')

def setup(n):
    return [[-1, 0] for i in range(n)]

def emptyBefore(n):
    for i in range(n):
        full()

def filledAfter(*args):
    args = args[0]
    for i in args:
        left(i[0]-1)
        brick(i[1])
        right(FIELD_LENGTH - i[0] + 1 - i[1])

def setbrick():
    global level, levels, pos, direction, brick_length, FIELD_LENGTH, FIELD_HEIGHT, game, win
    if level != FIELD_HEIGHT and (pos - direction != levels[level][0]):
        brick_length -= abs(pos - direction - levels[level][0])
        if pos - direction < levels[level][0]:
            pos = levels[level][0] + direction
    if level == 1 or brick_length < 1:
        game = False
        if brick_length < 1:
            win = False
    else:
        if (pos == 1) or (pos - 1 + brick_length == FIELD_LENGTH):
            levels[level - 1][0] = pos + direction
        else:
            levels[level - 1][0] = pos - direction
        levels[level - 1][1] = brick_length
        rand = randint(0,1)
        if rand == 1:
            pos = 1
            direction = 1
        else:
            pos = FIELD_LENGTH - brick_length + 1
            direction = -1
        level -= 1

def default():
    global pos, direction, brick_length, level, game, diff
    brick_length = diff
    direction = 1
    pos = 1
    level = FIELD_HEIGHT
    game = True

def greating():
    global lang, diff, brick_length, FIELD_LENGTH, FIELD_HEIGHT
    print('Select language:')
    print('ru - русский, en - english')
    lang = input().lower().strip()
    if lang not in LANGUAGES:
        lang = 'en'

    print(PHRASES['diff'][lang])
    try:
        diff = int(input())
        if diff not in range(1,5):
            diff = 3
    except:
        diff = 3

    print(PHRASES['size'][lang])
    try:
        FIELD_LENGTH, FIELD_HEIGHT = map(int, input().split())
        if FIELD_LENGTH < diff + 3:
            FIELD_LENGTH = 7
        if FIELD_HEIGHT < 4:
            FIELD_HEIGHT = 4
    except:
        FIELD_LENGTH, FIELD_HEIGHT = 15, 12

    print(PHRASES['hello'][lang])
    print(PHRASES['control'][lang])
    print(PHRASES['ready1'][lang])
    input()
    os.system('cls')
    for i in range(3,0,-1):
        print(PHRASES['hello'][lang])
        print(PHRASES['control'][lang])
        print(PHRASES['ready2'][lang])
        print(i)
        delay(1)
        os.system('cls')        
    os.system('cls')

def finish():
    global win, play
    if win == True:
        print(PHRASES['win'][lang])
        print(PHRASES['again'][lang])
    else:
        print(PHRASES['lose'][lang])
    print(PHRASES['YN'][lang])
    ans = input().strip()
    if ans == '2':
        play = False
    elif ans == '1':
        default()
    elif ans != '1':
        print(PHRASES['wrong'][lang])
        delay(2)
        play = False

game = True
win = True
play = True

#FIELD_LENGTH = 15
#FIELD_HEIGHT = 12
#START_BR_LENGTH = 3
BRICK_SYMB = '8'

DIFFICULTIES = {
    1: 0.01,
    2: 0.05,
    3: 0.2,
    4: 0.5
}
PHRASES = {
    'size': {'ru': 'Введи два числа: ширина и высота поля в клетках. (рекомендуется 15 и 12)', 'en': 'Enter two numbers: length and height of the field in squares. (recommend 15 and 12)'},
    'diff': {'ru': 'Выбери уровень сложности от 1 до 4 (1 - сложно).', 'en': 'Select difficulty from 1 to 4 (1 - very hard).'},
    'hello': {'ru': 'Привет! Это игра "Tower blocks".', 'en':'Hello! It`s "Tower blocks" game.'},
    'ready1': {'ru': 'Ты готов? (Нажми клавишу Enter)', 'en':'Are you ready? (press Enter key)'},
    'ready2': {'ru': 'Ты готов?', 'en': 'Are you ready?'},
    'control': {'ru': 'Поставить блок - пробел.', 'en': 'Press space key to place a block.'},
    'win': {'ru': 'Ты выиграл! Поздравляю!', 'en': 'You won! Congratulations!'},
    'lose': {'ru': 'Ты проиграл. :( Хочешь попробовать снова?', 'en': 'You lose. :( Try again?'},
    'again': {'ru': 'Ты хочешь поиграть снова?', 'en': 'Do you want to play again?'},
    'wrong': {'ru': 'Неправильный ответ', 'en': 'Wrong answer'},
    'YN': {'ru': 'Да - "1", Нет - "2"', 'en': 'Yes - "1", No - "2"'}
}
LANGUAGES = ('en', 'ru')

direction = 1
pos = 1

pygame.init()
sc = pygame.display.set_mode((700, 700))

greating()
level = FIELD_HEIGHT
brick_length = diff
levels = setup(FIELD_HEIGHT)

while play:
    while game:
        """print(pos, brick_length, end = '')
        try:
            print(levels[level][0])
        except:
            print()"""
        emptyBefore(level - 1)

        left(pos-1) #левая часть до кирпича
        brick(brick_length) #кирпич
        right(FIELD_LENGTH - pos + 1 - brick_length) #правая часть после кирпича
    
        filledAfter(levels[level:])

        shift() #сдвиг кирпича каждый ход
        delay(DIFFICULTIES[diff])
        os.system('cls')

        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE:
                setbrick()
            if i.type == pygame.QUIT:
                exit()
    finish()
