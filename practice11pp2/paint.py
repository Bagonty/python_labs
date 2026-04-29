import pygame
import sys
import math

# ------------------------------
# Window and toolbar settings
# ------------------------------
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
TOOLBAR_WIDTH = 180

# Canvas starts after the toolbar
CANVAS_X = TOOLBAR_WIDTH
CANVAS_Y = 0
CANVAS_W = SCREEN_WIDTH - TOOLBAR_WIDTH
CANVAS_H = SCREEN_HEIGHT

# ------------------------------
# Colors
# ------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (60, 60, 60)
BG_COLOR = (40, 40, 40)

# Available drawing colors
PALETTE = [
    (0, 0, 0), (255, 255, 255), (200, 20, 20), (220, 120, 30),
    (220, 220, 0), (20, 180, 20), (0, 150, 200), (30, 80, 200),
    (130, 30, 200), (200, 30, 140), (100, 100, 100), (160, 80, 20),
    (0, 200, 150), (255, 165, 0), (128, 0, 128), (0, 128, 128),
    (255, 105, 180), (144, 238, 144), (135, 206, 250), (255, 222, 173)
]

# Practice 11: added Square, Right Triangle, Equilateral Triangle and Rhombus
TOOLS = [
    "Pencil",
    "Rectangle",
    "Circle",
    "Square",
    "Right Triangle",
    "Equilateral",
    "Rhombus",
    "Eraser"
]


class Button:
    """
    Class for interface buttons.
    Each button has a rectangle area, label, color and active state.
    """
    def __init__(self, rect, label, color=DARK_GRAY, text_color=WHITE):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.color = color
        self.text_color = text_color
        self.active = False

    def draw(self, surface, font):
        """Draws the button. Active button is highlighted."""
        bg = (100, 180, 100) if self.active else self.color
        pygame.draw.rect(surface, bg, self.rect, border_radius=5)
        pygame.draw.rect(surface, LIGHT_GRAY, self.rect, 1, border_radius=5)

        text = font.render(self.label, True, self.text_color)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        """Checks whether the mouse position is inside the button."""
        return self.rect.collidepoint(pos)


def get_rect_from_points(start_pos, end_pos):
    """
    Creates a pygame.Rect using two points.
    This works even when the user drags the mouse in any direction.
    """
    sx, sy = start_pos
    ex, ey = end_pos
    return pygame.Rect(min(sx, ex), min(sy, ey), abs(ex - sx), abs(ey - sy))


def get_square_rect(start_pos, end_pos):
    """
    Creates a square from two points.
    The side size is based on the biggest mouse movement direction.
    """
    sx, sy = start_pos
    ex, ey = end_pos

    dx = ex - sx
    dy = ey - sy
    side = max(abs(dx), abs(dy))

    # Keep the direction of mouse dragging
    x = sx if dx >= 0 else sx - side
    y = sy if dy >= 0 else sy - side

    return pygame.Rect(x, y, side, side)


def get_right_triangle_points(start_pos, end_pos):
    """
    Creates points for a right triangle.
    The triangle is based on the rectangle between start and end positions.
    """
    sx, sy = start_pos
    ex, ey = end_pos

    return [
        (sx, sy),      # first point
        (ex, sy),      # horizontal point
        (sx, ey)       # vertical point
    ]


def get_equilateral_triangle_points(start_pos, end_pos):
    """
    Creates points for an equilateral triangle.
    All sides are approximately equal.
    """
    sx, sy = start_pos
    ex, ey = end_pos

    side = max(abs(ex - sx), abs(ey - sy))
    height = int(side * math.sqrt(3) / 2)

    # Direction depends on mouse movement
    direction_x = 1 if ex >= sx else -1
    direction_y = 1 if ey >= sy else -1

    top = (sx, sy)
    left = (sx - direction_x * side // 2, sy + direction_y * height)
    right = (sx + direction_x * side // 2, sy + direction_y * height)

    return [top, right, left]


def get_rhombus_points(start_pos, end_pos):
    """
    Creates points for a rhombus.
    A rhombus is drawn as a diamond shape inside the selected rectangle.
    """
    rect = get_rect_from_points(start_pos, end_pos)

    top = (rect.centerx, rect.top)
    right = (rect.right, rect.centery)
    bottom = (rect.centerx, rect.bottom)
    left = (rect.left, rect.centery)

    return [top, right, bottom, left]


def draw_shape(surface, tool, color, start_pos, end_pos, brush_size):
    """
    Draws the selected figure on the given surface.
    This function is used both for preview and for final drawing.
    """
    if tool == "Rectangle":
        rect = get_rect_from_points(start_pos, end_pos)
        pygame.draw.rect(surface, color, rect, brush_size)

    elif tool == "Circle":
        sx, sy = start_pos
        ex, ey = end_pos
        radius = max(abs(ex - sx), abs(ey - sy)) // 2
        if radius > 0:
            pygame.draw.circle(surface, color, ((sx + ex) // 2, (sy + ey) // 2), radius, brush_size)

    elif tool == "Square":
        rect = get_square_rect(start_pos, end_pos)
        pygame.draw.rect(surface, color, rect, brush_size)

    elif tool == "Right Triangle":
        points = get_right_triangle_points(start_pos, end_pos)
        pygame.draw.polygon(surface, color, points, brush_size)

    elif tool == "Equilateral":
        points = get_equilateral_triangle_points(start_pos, end_pos)
        pygame.draw.polygon(surface, color, points, brush_size)

    elif tool == "Rhombus":
        points = get_rhombus_points(start_pos, end_pos)
        pygame.draw.polygon(surface, color, points, brush_size)


def main():
    pygame.init()

    # Create program window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Paint Practice 11")

    clock = pygame.time.Clock()

    # Fonts for toolbar text
    font = pygame.font.SysFont("Arial", 12, bold=True)
    small = pygame.font.SysFont("Arial", 12)

    # Canvas is a separate surface where the drawing is stored
    canvas = pygame.Surface((CANVAS_W, CANVAS_H))
    canvas.fill(WHITE)

    # Current program state
    current_tool = "Pencil"
    draw_color = BLACK
    brush_size = 5
    eraser_size = 20
    drawing = False
    start_pos = None
    temp_canvas = None

    # Create buttons for all tools
    tool_buttons = []
    for i, name in enumerate(TOOLS):
        btn = Button((10, 45 + i * 35, TOOLBAR_WIDTH - 20, 30), name)
        if name == current_tool:
            btn.active = True
        tool_buttons.append(btn)

    # Brush size slider
    size_slider_rect = pygame.Rect(10, 335, TOOLBAR_WIDTH - 20, 10)
    MAX_BRUSH = 40

    # Color palette settings
    palette_start_y = 380
    swatch_size = 26
    cols_in_palette = 4

    # Clear canvas button
    clear_btn = Button((10, SCREEN_HEIGHT - 50, TOOLBAR_WIDTH - 20, 36), "Clear", color=(150, 40, 40))

    # Tools that are drawn by dragging the mouse from one point to another
    shape_tools = ("Rectangle", "Circle", "Square", "Right Triangle", "Equilateral", "Rhombus")

    while True:
        clock.tick(60)

        mouse_pos = pygame.mouse.get_pos()

        # Convert mouse coordinates from window coordinates to canvas coordinates
        canvas_mouse = (mouse_pos[0] - CANVAS_X, mouse_pos[1] - CANVAS_Y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Left mouse button pressed
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = mouse_pos

                # Click inside toolbar
                if mx < TOOLBAR_WIDTH:

                    # Tool selection
                    for btn in tool_buttons:
                        if btn.is_clicked(mouse_pos):
                            current_tool = btn.label
                            for b in tool_buttons:
                                b.active = False
                            btn.active = True

                    # Clear canvas
                    if clear_btn.is_clicked(mouse_pos):
                        canvas.fill(WHITE)

                    # Brush size slider
                    if size_slider_rect.collidepoint(mouse_pos):
                        ratio = (mx - size_slider_rect.x) / size_slider_rect.width
                        brush_size = max(1, min(MAX_BRUSH, int(ratio * MAX_BRUSH)))
                        eraser_size = brush_size * 4

                    # Color selection
                    for idx, color in enumerate(PALETTE):
                        sx = 10 + (idx % cols_in_palette) * (swatch_size + 4)
                        sy = palette_start_y + (idx // cols_in_palette) * (swatch_size + 4)

                        if pygame.Rect(sx, sy, swatch_size, swatch_size).collidepoint(mouse_pos):
                            draw_color = color
                            current_tool = "Pencil"
                            for b in tool_buttons:
                                b.active = (b.label == "Pencil")

                # Click inside canvas
                elif 0 <= canvas_mouse[0] < CANVAS_W and 0 <= canvas_mouse[1] < CANVAS_H:
                    drawing = True
                    start_pos = canvas_mouse

                    # Save canvas copy for preview of figures
                    temp_canvas = canvas.copy()

                    if current_tool == "Pencil":
                        pygame.draw.circle(canvas, draw_color, canvas_mouse, brush_size)

                    elif current_tool == "Eraser":
                        pygame.draw.circle(canvas, WHITE, canvas_mouse, eraser_size)

            # Left mouse button released
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing and start_pos and current_tool in shape_tools:
                    draw_shape(canvas, current_tool, draw_color, start_pos, canvas_mouse, brush_size)

                drawing = False
                start_pos = None
                temp_canvas = None

            # Mouse movement while drawing
            if event.type == pygame.MOUSEMOTION:
                if drawing and 0 <= canvas_mouse[0] < CANVAS_W and 0 <= canvas_mouse[1] < CANVAS_H:

                    # Pencil draws a smooth continuous line
                    if current_tool == "Pencil":
                        prev = (
                            event.pos[0] - event.rel[0] - CANVAS_X,
                            event.pos[1] - event.rel[1] - CANVAS_Y
                        )
                        pygame.draw.line(canvas, draw_color, prev, canvas_mouse, brush_size * 2)
                        pygame.draw.circle(canvas, draw_color, canvas_mouse, brush_size)

                    # Eraser works like drawing with white color
                    elif current_tool == "Eraser":
                        pygame.draw.circle(canvas, WHITE, canvas_mouse, eraser_size)

        # ------------------------------
        # Drawing the frame
        # ------------------------------
        screen.fill(BG_COLOR)

        # Preview for shape tools while dragging
        if drawing and temp_canvas and current_tool in shape_tools:
            preview = temp_canvas.copy()
            draw_shape(preview, current_tool, draw_color, start_pos, canvas_mouse, brush_size)
            screen.blit(preview, (CANVAS_X, CANVAS_Y))
        else:
            screen.blit(canvas, (CANVAS_X, CANVAS_Y))

        # Draw toolbar background
        pygame.draw.rect(screen, BG_COLOR, (0, 0, TOOLBAR_WIDTH, SCREEN_HEIGHT))
        pygame.draw.line(screen, LIGHT_GRAY, (TOOLBAR_WIDTH, 0), (TOOLBAR_WIDTH, SCREEN_HEIGHT), 1)

        # Toolbar title
        screen.blit(font.render("TOOLS", True, LIGHT_GRAY), (10, 10))

        # Draw tool buttons
        for btn in tool_buttons:
            btn.draw(screen, font)

        # Brush size text and slider
        screen.blit(font.render(f"Size: {brush_size}", True, LIGHT_GRAY), (10, 315))
        pygame.draw.rect(screen, LIGHT_GRAY, size_slider_rect)
        pygame.draw.rect(
            screen,
            (100, 200, 100),
            (
                size_slider_rect.x,
                size_slider_rect.y,
                int(size_slider_rect.width * brush_size / MAX_BRUSH),
                10
            )
        )
        pygame.draw.rect(screen, WHITE, size_slider_rect, 1)

        # Draw color palette
        screen.blit(font.render("Colors:", True, LIGHT_GRAY), (10, palette_start_y - 20))
        for idx, color in enumerate(PALETTE):
            sx = 10 + (idx % cols_in_palette) * (swatch_size + 4)
            sy = palette_start_y + (idx // cols_in_palette) * (swatch_size + 4)
            swatch = pygame.Rect(sx, sy, swatch_size, swatch_size)

            pygame.draw.rect(screen, color, swatch, border_radius=4)

            # Highlight selected color
            if color == draw_color:
                pygame.draw.rect(screen, WHITE, swatch, 2, border_radius=4)

        # Current selected color preview
        pygame.draw.rect(
            screen,
            draw_color,
            (10, palette_start_y + 140, TOOLBAR_WIDTH - 20, 28),
            border_radius=5
        )

        # Show eraser size only when eraser is selected
        if current_tool == "Eraser":
            screen.blit(small.render(f"Eraser: {eraser_size}px", True, LIGHT_GRAY), (10, palette_start_y + 175))

        clear_btn.draw(screen, font)

        # Update display
        pygame.display.flip()


if __name__ == "__main__":
    main()
