import math

a = [1,0,1]
b = [0,1,1]

def norm_vec(v):
    l = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    x = v[0] / l
    y = v[1] / l
    z = v[2] / l
    return [x,y,z]

def calc_angle(a,b):
    a = norm_vec(a)
    b = norm_vec(b)
    dot_product = a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    a_mag = math.sqrt(a[0]**2 + a[1]**2 + a[2]**2)
    b_mag = math.sqrt(b[0]**2 + b[1]**2 + b[2]**2)
    return math.acos(dot_product / (a_mag * b_mag))

print("angle is", calc_angle(a,b) / math.pi, 'times pi radians')