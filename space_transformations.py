import pygame, time, math, copy

class Line():
    def __init__(self, start_point, end_point, is_axis, color=None):
        self.start_point = start_point
        self.end_point = end_point
        self.is_axis = is_axis
        self.color = [255,0,0]
        if (is_axis):
            self.color = [0,255,0]
        if color != None:
            self.color = color

        self.points = {}
        delta_x = end_point[0] - start_point[0]
        delta_y = end_point[1] - start_point[1]
        points_needed = 30
        for point in range(int(points_needed) + 1):
            proportion = (point / points_needed)
            x = int(start_point[0] + (delta_x * proportion))
            y = int(start_point[1] + (delta_y * proportion))
            y_radius = Y_RANGE[1] + 1
            x_radius = X_RANGE[1] + 1
            # rather tricky math to project the screen location onto the y-axis location
            scaled_y = 2.0 * y_radius * (SCREEN_HEIGHT - y) / SCREEN_HEIGHT - y_radius
            # similar math for projection with x-axis
            scaled_x = 2.0 * x_radius * x / SCREEN_WIDTH - x_radius
            # transform the points projected onto the axis
            transformed_y = transform_y(scaled_y)
            transformed_x = transform_x(scaled_x)
            transformed_x, transformed_y = matrix_transform(scaled_x,scaled_y)
            # more tricky math to project the axis onto the screen location
            animation_delta_y = SCREEN_HEIGHT * (y_radius - transformed_y) / (2.0 * y_radius) - y
            # similar math for x-projection
            animation_delta_x = SCREEN_WIDTH * (x_radius + transformed_x) / (2.0 * x_radius) - x
            self.points[(x,y)] = (animation_delta_x, animation_delta_y)

    def animate(self, proportion):
        animated_points = [[point[0] + (self.points[point][0] * proportion), point[1] + (self.points[point][1] * proportion)] for point in self.points]
        pygame.draw.lines(screen, self.color, False, animated_points, 4)

    def draw_base_line(self):
        pygame.draw.line(screen, [255,255,255], self.start_point, self.end_point, 2)

def matrix_transform(x, y):
    print('inital x, y is', x, y)
    matrix = [[2,2],
              [3,-1]]
    transformed_x = x * matrix[0][0] + y * matrix[0][1]
    transformed_y = x * matrix[1][0] + y * matrix[1][1]
    print('final x, y is', transformed_x, transformed_y)
    return (transformed_x,transformed_y)

def transform_y(y):
    return y

def transform_x(x):
    return x*3

def make_lines():
    lines = []
    x_spacing = SCREEN_WIDTH // (X_RANGE[1] - X_RANGE[0] + 2)
    y_spacing = SCREEN_HEIGHT // (Y_RANGE[1] - Y_RANGE[0] + 2)
    spacing = x_spacing
    for x_line in range(X_RANGE[0], X_RANGE[1] + 1):
        lines.append(Line([spacing, 0], [spacing, SCREEN_HEIGHT], False))
        spacing += x_spacing
    spacing = y_spacing
    for y_line in range(Y_RANGE[0], Y_RANGE[1] + 1):
        lines.append(Line([0, spacing], [SCREEN_WIDTH, spacing], False))
        spacing += y_spacing
    lines.append(Line([SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], [SCREEN_WIDTH // 2 + x_spacing, SCREEN_HEIGHT // 2], True, color = [0,255,250]))
    lines.append(Line([SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - y_spacing], True))
    #lines.append(Line([0,SCREEN_HEIGHT], [SCREEN_WIDTH, 0], True))
    return lines

X_RANGE = (-4,4)
Y_RANGE = (-4,4)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = [50,50,50]
AXIS_COLOR = [255,255,255]
ANIMATE_TIME = 12

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
            line.draw_base_line()
        for line in lines:
            line.animate(running_time / ANIMATE_TIME)
        pygame.display.flip()
    time.sleep(delta_time)