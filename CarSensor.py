import numpy as np
import pyglet
from GameGeometry import LineSegment, Point

class Sensor:
    def __init__(self, P_s, P_v, length, ID):
        self.id = ID
        self.direction = LineSegment(P_s, P_v)
        self.max_length = length
        self.angle = self.direction.get_angle()
        
        self.ray_end_point = Point()
        self.sensor_ray = LineSegment(self.direction.b, self.ray_end_point)
        
        self.distance = self.max_length
        
        self.label = pyglet.text.Label('Sensor' + str(self.id) + ': ' + str(self.distance), 
                          font_name='Times New Roman', 
                          font_size=15,
                          x=10, y=self.id*18)
        
    def draw(self):
#        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
#                                 ('v2f', (self.sensor_ray.a.x, self.sensor_ray.a.y, 
#                                          self.sensor_ray.b.x, self.sensor_ray.b.y)))
#        
        self.label.draw()
        
    def update(self):
        self.angle = self.direction.get_angle()
        self.ray_end_point.x = self.direction.b.x + self.max_length*np.cos(np.radians(self.angle))*(-1)
        self.ray_end_point.y = self.direction.b.y + self.max_length*np.sin(np.radians(self.angle))
        self.label.text = 'Sensor' + str(self.id) + ': ' + str(self.distance)
        