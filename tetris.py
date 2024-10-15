import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Размер экрана
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Установим размер сетки
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Настройки экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Тетрис")

# Создаем фигуры Тетриса
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],
    
    [[0, 1, 1],
     [1, 1, 0]],
    
    [[1, 1, 0],
     [0, 1, 1]],
    
    [[1, 1, 1, 1]],
    
    [[1, 1],
     [1, 1]],
    
    [[1, 1, 1],
     [1, 0, 0]],
    
    [[1, 1, 1],
     [0, 0, 1]]
]

# Определение класса фигур
class Shape:
    def __init__(self, shape):
        self.shape = shape
        self.y = 0
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Создание игровой сетки
grid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

def check_collision(shape, offset_x, offset_y):
    for y, row in enumerate(shape.shape):
        for x, cell in enumerate(row):
            if cell:
                try:
                    if grid[y + shape.y + offset_y][x + shape.x + offset_x]:
                        return True
                except IndexError:
                    return True
    return False

def merge_shape(shape):
    for y, row in enumerate(shape.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[y + shape.y][x + shape.x] = 1

def remove_full_lines():
    global grid
    grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(grid) < GRID_HEIGHT:
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])

# Основная функция игры
def run_game():
    clock = pygame.time.Clock()
    shape = Shape(random.choice(SHAPES))
    game_over = False
    score = 0

    while not game_over:
        screen.fill(BLACK)
        
        # Отрисовка сетки
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if grid[y][x]:
                    pygame.draw.rect(screen, BLUE, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Отрисовка падающей фигуры
        for y, row in enumerate(shape.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, GREEN, pygame.Rect((shape.x + x) * BLOCK_SIZE, (shape.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.update()

        # Контроль ввода
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(shape, -1, 0):
                    shape.x -= 1
                if event.key == pygame.K_RIGHT and not check_collision(shape, 1, 0):
                    shape.x += 1
                if event.key == pygame.K_DOWN and not check_collision(shape, 0, 1):
                    shape.y += 1
                if event.key == pygame.K_UP:
                    shape.rotate()
                    if check_collision(shape, 0, 0):
                        shape.rotate()
                        shape.rotate()
                        shape.rotate()

        # Автоматическое падение фигуры вниз
        if not check_collision(shape, 0, 1):
            shape.y += 1
        else:
            merge_shape(shape)
            remove_full_lines()
            shape = Shape(random.choice(SHAPES))
            if check_collision(shape, 0, 0):
                game_over = True

        clock.tick(2)

    print("Игра окончена!")

# Запуск игры
run_game()
pygame.quit()
