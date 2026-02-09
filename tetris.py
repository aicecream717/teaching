import pygame
import random
from dataclasses import dataclass

CELL_SIZE = 30
COLS = 10
ROWS = 20
FPS = 60

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

BACKGROUND = (18, 18, 18)
GRID_COLOR = (40, 40, 40)
TEXT_COLOR = (240, 240, 240)

SHAPES = {
    "I": [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
    ],
    "O": [
        [(1, 0), (2, 0), (1, 1), (2, 1)],
    ],
    "T": [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
    ],
    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
    ],
    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
}

COLORS = {
    "I": (77, 208, 225),
    "O": (255, 241, 118),
    "T": (171, 71, 188),
    "S": (129, 199, 132),
    "Z": (229, 115, 115),
    "J": (100, 181, 246),
    "L": (255, 167, 38),
}


@dataclass
class Piece:
    shape: str
    rotation: int
    x: int
    y: int

    @property
    def blocks(self):
        rotations = SHAPES[self.shape]
        rotation = rotations[self.rotation % len(rotations)]
        return [(self.x + dx, self.y + dy) for dx, dy in rotation]


def create_bag():
    bag = list(SHAPES.keys())
    random.shuffle(bag)
    return bag


def draw_grid(surface):
    for x in range(COLS):
        pygame.draw.line(surface, GRID_COLOR, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
    for y in range(ROWS):
        pygame.draw.line(surface, GRID_COLOR, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))


def draw_cell(surface, x, y, color):
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (0, 0, 0), rect, 1)


def is_valid_position(piece, board):
    for x, y in piece.blocks:
        if x < 0 or x >= COLS or y < 0 or y >= ROWS:
            return False
        if board[y][x] is not None:
            return False
    return True


def lock_piece(piece, board):
    for x, y in piece.blocks:
        board[y][x] = piece.shape


def clear_lines(board):
    new_board = [row for row in board if any(cell is None for cell in row)]
    cleared = ROWS - len(new_board)
    for _ in range(cleared):
        new_board.insert(0, [None for _ in range(COLS)])
    return new_board, cleared


def draw_board(surface, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                draw_cell(surface, x, y, COLORS[cell])


def draw_piece(surface, piece):
    for x, y in piece.blocks:
        draw_cell(surface, x, y, COLORS[piece.shape])


def draw_hud(surface, score, level, lines, font):
    text = font.render(f"Score: {score}  Lines: {lines}  Level: {level}", True, TEXT_COLOR)
    surface.blit(text, (10, 10))


def next_fall_time(level):
    return max(120, 700 - level * 50)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    bag = create_bag()
    score = 0
    lines = 0
    level = 1

    current = Piece(bag.pop(), 0, COLS // 2 - 2, 0)
    next_piece = Piece(bag.pop(), 0, COLS // 2 - 2, 0)

    fall_timer = 0
    running = True

    while running:
        delta = clock.tick(FPS)
        fall_timer += delta

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moved = Piece(current.shape, current.rotation, current.x - 1, current.y)
                    if is_valid_position(moved, board):
                        current = moved
                elif event.key == pygame.K_RIGHT:
                    moved = Piece(current.shape, current.rotation, current.x + 1, current.y)
                    if is_valid_position(moved, board):
                        current = moved
                elif event.key == pygame.K_DOWN:
                    moved = Piece(current.shape, current.rotation, current.x, current.y + 1)
                    if is_valid_position(moved, board):
                        current = moved
                elif event.key == pygame.K_UP:
                    rotated = Piece(current.shape, current.rotation + 1, current.x, current.y)
                    if is_valid_position(rotated, board):
                        current = rotated
                elif event.key == pygame.K_SPACE:
                    dropped = Piece(current.shape, current.rotation, current.x, current.y)
                    while is_valid_position(Piece(dropped.shape, dropped.rotation, dropped.x, dropped.y + 1), board):
                        dropped = Piece(dropped.shape, dropped.rotation, dropped.x, dropped.y + 1)
                    current = dropped
                    fall_timer = next_fall_time(level)

        if fall_timer >= next_fall_time(level):
            fall_timer = 0
            moved = Piece(current.shape, current.rotation, current.x, current.y + 1)
            if is_valid_position(moved, board):
                current = moved
            else:
                lock_piece(current, board)
                board, cleared = clear_lines(board)
                if cleared:
                    lines += cleared
                    score += (100 * cleared) * level
                    level = 1 + lines // 10

                if not bag:
                    bag = create_bag()
                current = next_piece
                current = Piece(current.shape, 0, COLS // 2 - 2, 0)
                if not bag:
                    bag = create_bag()
                next_piece = Piece(bag.pop(), 0, COLS // 2 - 2, 0)

                if not is_valid_position(current, board):
                    running = False

        screen.fill(BACKGROUND)
        draw_grid(screen)
        draw_board(screen, board)
        draw_piece(screen, current)
        draw_hud(screen, score, level, lines, font)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
