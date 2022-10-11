from __future__ import division
import numpy as np

EPSILON = 0.00000001

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
#prima 2 tocke
class LineSegment:
    def __init__(self, P_a, P_b):
        self.a = P_a
        self.b = P_b
    
    def get_bounding_box(self):
        box = []
        box.append(np.minimum(self.a.x, self.b.x))
        box.append(np.minimum(self.a.y, self.b.y))
        box.append(np.maximum(self.a.x, self.b.x))
        box.append(np.maximum(self.a.y, self.b.y))
        return box
    
    def get_angle(self):
        angle = 0
        if(np.abs((self.a.x-self.b.x)) < EPSILON):
            angle = np.degrees(np.arctan((self.a.y-self.b.y)/EPSILON))*(-1)
        angle = np.degrees(np.arctan((self.a.y-self.b.y)/(self.a.x-self.b.x)))*(-1)
        if (self.a.x-self.b.x) < 0:
            angle += 180
        return angle

# Collision detection
    
def cross_product(a, b):
    return a.x*b.y - b.x*a.y

def do_bounding_boxes_intersect(box_a, box_b):
    return ((box_a[0] <= box_b[2]) and 
            (box_a[2] >= box_b[0]) and 
            (box_a[1] <= box_b[3]) and 
            (box_a[3] >= box_b[1]))

def is_point_on_line(LS_a, P_b):
    aTmp = LineSegment(Point(), Point(LS_a.b.x-LS_a.a.x, LS_a.b.y-LS_a.a.y))
    bTmp = Point(P_b.x-LS_a.a.x, P_b.y-LS_a.a.y)
    r = cross_product(aTmp.b, bTmp)
    return np.abs(r) < EPSILON
    
def is_point_right_of_line(LS_a, P_b):
    aTmp = LineSegment(Point(), Point(LS_a.b.x-LS_a.a.x, LS_a.b.y-LS_a.a.y))
    bTmp = Point(P_b.x-LS_a.a.x, P_b.y-LS_a.a.y)
    return cross_product(aTmp.b, bTmp) < 0

def line_segment_touches_or_crosses_line(LS_a, LS_b):
    return (is_point_on_line(LS_a, LS_b.a) or 
            is_point_on_line(LS_a, LS_b.b) or 
            (is_point_right_of_line(LS_a, LS_b.a) ^ is_point_right_of_line(LS_a, LS_b.b)))
    
def do_lines_intersect(LS_a, LS_b):
    box1 = LS_a.get_bounding_box()
    box2 = LS_b.get_bounding_box()
    return (do_bounding_boxes_intersect(box1, box2) and 
            line_segment_touches_or_crosses_line(LS_a, LS_b) and 
            line_segment_touches_or_crosses_line(LS_b, LS_a))

def distance_between_two_points(P_a, P_b):
    return np.sqrt((np.power((P_b.x-P_a.x), 2) + np.power((P_b.y-P_a.y), 2)))

# 2 Line segment intersection

def perp(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def segment_intersect(a1, a2, b1, b2):
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = np.dot(dap, db)
    num = np.dot(dap, dp)
    if(denom == 0):
        return (num/EPSILON)*db + b1
    return (num/denom.astype(float))*db + b1
