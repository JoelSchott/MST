x_0 = input('What is the initial x? :')
v_0 = input('What is the initial velocity? :')
a = input('What is the constant acceleration? :')
max_x = input('What is the max x? :')
zero_x = input("When is x zero? :")

def get_position(x, v, a, t):
    return x + (v*t) + float(1/2)*a*(t**2)
