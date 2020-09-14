import pygame, time, math, copy

class Line():
    def __init__(self, start_point, end_point, is_axis):
        self.start_point = start_point
        self.end_point = end_point
        self.is_axis = is_axis
        self.color = AXIS_COLOR
        if (is_axis):
            self.color = [255,0,0]

        self.points = {}
        delta_x = end_point[0] - start_point[0]
        delta_y = end_point[1] - start_point[1]
        points_needed = 30
        for point in range(int(points_needed) + 1):
            proportion = (point / points_needed)
            x = int(start_point[0] + (delta_x * proportion))
            y = int(start_point[1] + (delta_y * proportion))
            y_radius = Y_RANGE[1] + 1
            # rather tricky math to project the screen location onto the axis location
            scaled_y = 2.0 * y_radius * (SCREEN_HEIGHT - y) / SCREEN_HEIGHT - y_radius
            # more tricky math to project the axis onto the screen location
            animation_delta_y = SCREEN_HEIGHT * (y_radius - transform(scaled_y)) / (2.0 * y_radius) - y
            print(animation_delta_y)
            self.points[(x,y)] = animation_delta_y

    def animate(self, proportion):
        animated_points = [[point[0], point[1] + (self.points[point] * proportion)] for point in self.points]
        pygame.draw.lines(screen, [0,255,0], False, animated_points, 2)

    def draw_base_line(self):
        pygame.draw.line(screen, self.color, self.start_point, self.end_point, 2)


def transform(x):
    return x**2 - 2*x - 1

def make_lines():
    lines = []
    x_spacing = SCREEN_WIDTH // (X_RANGE[1] - X_RANGE[0] + 2)
    y_spacing = SCREEN_HEIGHT // (Y_RANGE[1] - Y_RANGE[0] + 2)
    spacing = x_spacing
    for x_line in range(X_RANGE[0], X_RANGE[1] + 1):
        lines.append(Line([spacing, 0], [spacing, SCREEN_HEIGHT], x_line == 0))
        spacing += x_spacing
    spacing = y_spacing
    for y_line in range(Y_RANGE[0], Y_RANGE[1] + 1):
        lines.append(Line([0, spacing], [SCREEN_WIDTH, spacing], y_line == 0))
        spacing += y_spacing
    lines.append(Line([0,SCREEN_HEIGHT], [SCREEN_WIDTH, 0], True))
    return lines

X_RANGE = (-4,4)
Y_RANGE = (-4,4)
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
BACKGROUND_COLOR = [0,0,0]
AXIS_COLOR = [255,255,255]
ANIMATE_TIME = 5

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen.fill(BACKGROUND_COLOR)
pygame.display.flip()

lines = make_lines()

running_time = 0
delta_time = 0.05
running = True
while(running):
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if running_time < ANIMATE_TIME:
        running_time += delta_time
        for line in lines:
            line.animate(running_time / ANIMATE_TIME)
            if line.is_axis:
                line.draw_base_line()
            pygame.display.flip()
    time.sleep(delta_time)