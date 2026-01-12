import math

def angle_to_vector(a):
    return math.cos(a), math.sin(a)

def distance(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])
