import pygame
import random
import sys

# ------------------------------
# Grid and window settings
# ------------------------------
CELL = 20
COLS = 30
ROWS = 25
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL

# Game speed settings
FPS_BASE = 8
FPS_STEP = 2
FOOD_PER_LEVEL = 3

# Practice 11 additions
FOOD_VALUES = [1, 3, 5]       # Different food weights
FOOD_LIFETIME = 5000          # Food disappears after 5000 ms = 5 seconds

# ------------------------------
# Colors
# ------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 160, 0)
GREEN = (0, 200, 0)
RED = (220, 30, 30)
YELLOW = (255, 215, 0)
PURPLE = (180, 0, 180)
WALL_COLOR = (80, 80, 80)
BG_COLOR = (15, 15, 15)
GRID_COLOR = (25, 25, 25)

# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def draw_grid(surface):
    """Draw background grid."""
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y))


def draw_walls(surface):
    """Draw border walls."""
    pygame.draw.rect(surface, WALL_COLOR, (0, 0, WIDTH, CELL))
    pygame.draw.rect(surface, WALL_COLOR, (0, HEIGHT - CELL, WIDTH, CELL))
    pygame.draw.rect(surface, WALL_COLOR, (0, 0, CELL, HEIGHT))
    pygame.draw.rect(surface, WALL_COLOR, (WIDTH - CELL, 0, CELL, HEIGHT))


def cell_rect(col, row):
    """Convert grid cell coordinates to pygame Rect."""
    return pygame.Rect(col * CELL, row * CELL, CELL, CELL)


def random_food_position(snake_body):
    """
    Generate random food position.
    Food cannot appear on the snake body or inside the walls.
    """
    while True:
        col = random.randint(1, COLS - 2)
        row = random.randint(1, ROWS - 2)

        if (col, row) not in snake_body:
            return col, row


def create_food(snake_body):
    """
    Create food with random position and random weight.
    Practice 11 requirement:
    randomly generating food with different weights.
    """
    position = random_food_position(snake_body)
    value = random.choice(FOOD_VALUES)
    spawn_time = pygame.time.get_ticks()

    return {
        "pos": position,
        "value": value,
        "spawn_time": spawn_time
    }


def get_food_color(value):
    """Return food color depending on its value."""
    if value == 1:
        return RED
    elif value == 3:
        return YELLOW
    else:
        return PURPLE


def draw_food(surface, font, food):
    """Draw food and its value."""
    col, row = food["pos"]
    value = food["value"]

    rect = cell_rect(col, row).inflate(-4, -4)
    pygame.draw.ellipse(surface, get_food_color(value), rect)

    # Draw value number inside food
    label = font.render(str(value), True, BLACK)
    surface.blit(label, label.get_rect(center=rect.center))


def draw_hud(surface, font, score, level, food):
    """Draw score, level and food disappearing timer."""
    score_surf = font.render(f"Score: {score}", True, WHITE)
    level_surf = font.render(f"Level: {level}", True, YELLOW)

    surface.blit(score_surf, (CELL + 4, 2))
    surface.blit(level_surf, (WIDTH // 2 - level_surf.get_width() // 2, 2))

    # Show how many seconds food has left before disappearing
    time_left = max(0, (FOOD_LIFETIME - (pygame.time.get_ticks() - food["spawn_time"])) // 1000 + 1)
    timer_surf = font.render(f"Food time: {time_left}", True, WHITE)
    surface.blit(timer_surf, (WIDTH - timer_surf.get_width() - CELL, 2))


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Practice 11")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Consolas", 18, bold=True)
    big_font = pygame.font.SysFont("Consolas", 40, bold=True)

    # Initial snake body.
    # Each tuple is one body segment in grid coordinates.
    snake = [
        (COLS // 2, ROWS // 2),
        (COLS // 2 - 1, ROWS // 2),
        (COLS // 2 - 2, ROWS // 2)
    ]

    direction = RIGHT
    next_direction = RIGHT

    # Food is now stored as dictionary:
    # position + value + spawn time
    food = create_food(set(snake))

    score = 0
    level = 1
    food_eaten = 0
    fps = FPS_BASE
    game_over = False
    grow = False

    # Custom pygame event for snake movement.
    # Snake moves by timer, not every frame.
    STEP_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(STEP_EVENT, 1000 // fps)

    while True:
        clock.tick(60)

        # ------------------------------
        # Event handling
        # ------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Change direction.
                # Opposite direction is forbidden to avoid instant self-collision.
                if event.key == pygame.K_UP and direction != DOWN:
                    next_direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    next_direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    next_direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    next_direction = RIGHT

                # Restart game after game over
                if event.key == pygame.K_r and game_over:
                    main()
                    return

            # Snake movement step
            if event.type == STEP_EVENT and not game_over:
                direction = next_direction

                head_col, head_row = snake[0]
                dc, dr = direction

                new_head = (head_col + dc, head_row + dr)
                new_col, new_row = new_head

                # Check wall collision
                if new_col <= 0 or new_col >= COLS - 1 or new_row <= 0 or new_row >= ROWS - 1:
                    game_over = True
                    continue

                # Check self collision
                if new_head in snake:
                    game_over = True
                    continue

                # Add new head
                snake.insert(0, new_head)

                # Check food collision
                if new_head == food["pos"]:
                    # Score depends on food weight
                    score += food["value"] * 10
                    food_eaten += 1

                    # Create new random weighted food
                    food = create_food(set(snake))
                    grow = True

                    # Level up after eating several foods
                    if food_eaten >= FOOD_PER_LEVEL:
                        level += 1
                        food_eaten = 0

                        fps = FPS_BASE + (level - 1) * FPS_STEP
                        pygame.time.set_timer(STEP_EVENT, 1000 // fps)

                # If snake did not eat food, remove tail.
                # If it ate food, tail is not removed and snake becomes longer.
                if grow:
                    grow = False
                else:
                    snake.pop()

        # ------------------------------
        # Practice 11 food timer
        # ------------------------------
        # If food exists for too long, it disappears and new food appears.
        if not game_over:
            current_time = pygame.time.get_ticks()

            if current_time - food["spawn_time"] >= FOOD_LIFETIME:
                food = create_food(set(snake))

        # ------------------------------
        # Drawing
        # ------------------------------
        screen.fill(BG_COLOR)
        draw_grid(screen)
        draw_walls(screen)

        # Draw snake
        for i, (col, row) in enumerate(snake):
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(screen, color, cell_rect(col, row))
            pygame.draw.rect(screen, BLACK, cell_rect(col, row), 1)

        # Draw weighted food
        draw_food(screen, font, food)

        # Draw interface
        draw_hud(screen, font, score, level, food)

        # Game over screen
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))

            over = big_font.render("GAME OVER", True, RED)
            info = font.render(f"Score: {score} | Level: {level}", True, WHITE)
            restart = font.render("Press R to restart", True, YELLOW)

            screen.blit(over, over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
            screen.blit(info, info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))
            screen.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

        pygame.display.flip()


if __name__ == "__main__":
    main()
