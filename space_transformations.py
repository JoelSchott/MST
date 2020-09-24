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
        points_needed = 50
        for point in range(int(points_needed) + 1):
            proportion = (point / points_needed)
            x = int(start_point[0] + (delta_x * proportion))
            y = int(start_point[1] + (delta_y * proportion))

            self.points[(x,y)] = ()

    def generate_points(self, mat1 = None, mat2 = None, linear = True):
        new_points = {}
        for point in self.points.keys():
            if linear:
                initial_x, initial_y = mat_2x2_transform(mat1, x_screen_to_coord(point[0]), y_screen_to_coord(point[1]))
            else:
                initial_x, initial_y = x_screen_to_coord(point[0]), y_screen_to_coord(point[1])
            if linear:
                final_x, final_y = mat_2x2_transform(mat2, initial_x, initial_y)
            else:
                final_x, final_y = non_linear_transform(initial_x, initial_y)
            initial_x = x_coord_to_screen(initial_x)
            initial_y = y_coord_to_screen(initial_y)
            delta_x = x_coord_to_screen(final_x) - initial_x
            delta_y = y_coord_to_screen(final_y) - initial_y
            new_points[(initial_x, initial_y)] = (delta_x, delta_y)
        self.points = new_points

    def animate(self, proportion):
        animated_points = [[point[0] + (self.points[point][0] * proportion), point[1] + (self.points[point][1] * proportion)] for point in self.points]
        pygame.draw.lines(screen, self.color, False, animated_points, 4)

    def draw_base_line(self):
        pygame.draw.line(screen, [255,255,255], self.start_point, self.end_point, 2)

def x_screen_to_coord(x):
    # rather tricky math to project the screen location onto the x-axis location
    x_radius = X_RANGE[1] + 1
    return 2.0 * x_radius * x / SCREEN_WIDTH - x_radius

def y_screen_to_coord(y):
    # rather tricky math to project the screen location onto the y-axis location
    y_radius = Y_RANGE[1] + 1
    return 2.0 * y_radius * (SCREEN_HEIGHT - y) / SCREEN_HEIGHT - y_radius

def x_coord_to_screen(x):
    # projection from coordinate position to location on screen
    x_radius = X_RANGE[1] + 1
    return SCREEN_WIDTH * (x_radius + x) / (2.0 * x_radius)

def y_coord_to_screen(y):
    # projection from y coordinate to screen location
    y_radius = Y_RANGE[1] + 1
    return SCREEN_HEIGHT * (y_radius - y) / (2.0 * y_radius)

def mat_2x2_transform(matrix, x, y):
    transformed_x = x * matrix[0][0] + y * matrix[0][1]
    transformed_y = x * matrix[1][0] + y * matrix[1][1]
    return (transformed_x,transformed_y)

def mat_2x2_angular_transform(theta):
    matrix = [[math.cos(theta), math.cos(theta + math.pi / 2)],
                    [math.sin(theta), math.sin(theta + math.pi / 2)]]
    return matrix

def mat_2x2_inverse_transform(matrix):
    determinant = matrix[1][1] * matrix[0][0] - matrix[0][1] * matrix[1][0]
    inverse_matrix = [[matrix[1][1] / determinant, -matrix[0][1] / determinant],
                      [-matrix[1][0] / determinant, matrix[0][0] / determinant]]
    return inverse_matrix

def non_linear_transform(x, y):
    return transform_x(x), transform_y(y)

def transform_y(y):
    return 4 * math.sin(y)

def transform_x(x):
    return 4 * math.cos(x)

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
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = [50,50,50]
AXIS_COLOR = [255,255,255]
ANIMATE_TIME = 5

matrices = [[[0,1],
            [1,0]],[[2,-1],
                    [-1,2]]]

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen.fill(BACKGROUND_COLOR)
pygame.display.flip()

lines = make_lines()
for line in lines:
    line.generate_points(matrices[0], matrices[1], linear = True)

animations_run = 0
running_time = 0
delta_time = 0.05
running = True

while(running):
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if running_time < ANIMATE_TIME:

        for line in lines:
            line.draw_base_line()
        for line in lines:
            line.animate(running_time / ANIMATE_TIME)
        pygame.display.flip()
        if running_time == 0:
            time.sleep(2)
        running_time += delta_time
    else:
        animations_run += 1
        if animations_run == 1:
            running_time = 0
            for line in lines:
                line.generate_points(matrices[1], mat_2x2_inverse_transform(matrices[1]))
                line.draw_base_line()
                line.animate(0)
            x_spacing = SCREEN_WIDTH // (X_RANGE[1] - X_RANGE[0] + 2)
            y_spacing = SCREEN_HEIGHT // (Y_RANGE[1] - Y_RANGE[0] + 2)
            i_hat = Line([SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], [SCREEN_WIDTH // 2 + x_spacing, SCREEN_HEIGHT // 2], True, color = [255,255,0])
            i_hat.generate_points(matrices[0], mat_2x2_inverse_transform(matrices[1]))
            i_hat.animate(0)
            j_hat = Line([SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - y_spacing], True, color = [255,0,255])
            j_hat.generate_points(matrices[0], mat_2x2_inverse_transform(matrices[1]))
            j_hat.animate(0)
            lines.append(i_hat)
            lines.append(j_hat)
            pygame.display.flip()
            time.sleep(5)

    time.sleep(delta_time)