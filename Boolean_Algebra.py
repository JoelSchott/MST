import pygame, math, time

screen_width = 600
screen_height = 600

a_loc = [screen_width/3.0, screen_height/3.0]
b_loc = [screen_width*2.0/3.0, screen_height/3.0]
c_loc = [screen_width/2.0, screen_height*2.0/3.0]
x_radius = screen_width / 6.0
y_radius = screen_height / 6.0
circle_radius = math.sqrt(x_radius*x_radius + y_radius*y_radius)

class Circle:
    def __init__(self, loc):
        self.loc = [int(loc[0]), int(loc[1])]
    def inside(self, point):
        dx = point[0] - self.loc[0]
        dy = point[1] - self.loc[1]
        distance = math.sqrt(dx*dx + dy*dy)
        if distance < circle_radius:
            return True
        return False
    def draw(self):
        pygame.draw.circle(screen, [0,0,255], self.loc, int(circle_radius), 3)

def update_screen(click_point):
    circles = [a.inside(click_point), b.inside(click_point), c.inside(click_point)]
    for x in range(screen_width):
        for y in range(screen_height):
            inside = [a.inside([x,y]), b.inside([x,y]), c.inside([x,y])]
            if inside == circles:
                if screen.get_at((x,y)) == (150,150,150, 255):
                    screen.set_at((x,y), [0,0,0])
                else:
                    screen.set_at((x,y), [150,150,150])
    draw_circles()

def perform_not():
    for x in range(screen_width):
        for y in range(screen_height):
            if screen.get_at((x,y)) == (150,150,150, 255):
                screen.set_at((x,y), [0,0,0])
            else:
                screen.set_at((x,y), [150,150,150])
    draw_circles()

def draw_circles():
    a.draw()
    b.draw()
    c.draw()
    pygame.draw


a = Circle(a_loc)
b = Circle(b_loc)
c = Circle(c_loc)

pygame.init()
screen = pygame.display.set_mode([screen_width, screen_height])
screen.fill([0,0,0])
update_screen([0,0])

running = True
while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            update_screen(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if pygame.K_n:
                perform_not()

        pygame.display.flip()
    time.sleep(0.01)


