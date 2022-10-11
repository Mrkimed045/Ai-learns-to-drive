from __future__ import division
import pyglet
import numpy as np
from GameGeometry import Point, LineSegment, EPSILON
from CarSensor import Sensor
from CarNeuralNetwork import NeuralNetwork, INPUT_SIZE, HIDDEN1_LAYER_SIZE, HIDDEN2_LAYER_SIZE, OUTPUT_SIZE

def preload_image(image):
    img = pyglet.image.load('res/sprites/' + image)
    img.anchor_x = img.width // 4       # // = integer divider , width sa 4 djelim da mi je anchor na sredini zadnijh kotača
    img.anchor_y = img.height // 2
    return img

class Car:
    def __init__(self, sprite=None):
        self.init_posx = 0
        self.init_posy = -50
        self.init_rotation = 0
        
        self.posx = self.init_posx
        self.posy = self.init_posy
        self.vel = 0
        self.max_vel = 220
        self.min_vel = 0
        self.acc = 2
        self.max_rotation = 3
        self.rot_val = 3
        
        self.key_right = False
        self.key_left = False
        self.key_up = False
        self.key_down = False
        self.key_space = False
        
        self.car_placed = False
        self.car_ready = False   
        self.crash = False
        self.reward = False
        
        if sprite is not None:
            self.sprite = sprite
            self.sprite.x = self.posx
            self.sprite.y = self.posy
            self.sprite.scale = 0.25
            self.width = self.sprite.width
            self.height = self.sprite.height
            
        self.center = Point(self.posx + 0.25*self.width*np.cos(np.radians(self.sprite.rotation)),
                           self.posy + 0.25*self.width*np.sin(np.radians(self.sprite.rotation))*(-1))
        
        self.front = Point(self.posx + 0.75*self.width*np.cos(np.radians(self.sprite.rotation)),
                           self.posy + 0.75*self.width*np.sin(np.radians(self.sprite.rotation))*(-1))
        
        self.back = Point(self.posx + 0.25*self.width*np.cos(np.radians(self.sprite.rotation + 180)), 
                          self.posx + 0.25*self.width*np.sin(np.radians(self.sprite.rotation + 180))*(-1))
    
        self.left = Point()
        self.right = Point()
        self.front_left = Point()
        self.front_right = Point()
        self.back_left = Point()
        self.back_right = Point()
        self.front_left_middle = Point()
        self.front_right_middle = Point()
        
        self.front_line = LineSegment(self.front_left, self.front_right)
        self.right_line = LineSegment(self.front_right, self.back_right)
        self.back_line = LineSegment(self.back_left, self.back_right)
        self.left_line = LineSegment(self.front_left, self.back_left)
         
        self.sensors = []
        self.sensors.append(Sensor(self.center, self.front, 300, 1))
        self.sensors.append(Sensor(self.center, self.front_left, 300, 2))
        self.sensors.append(Sensor(self.center, self.front_right, 300, 3))
        self.sensors.append(Sensor(self.center, self.left, 300, 4))
        self.sensors.append(Sensor(self.center, self.right, 300, 5))
#       self.sensors.append(Sensor(self.center, self.back, 300, 6))
#       self.sensors.append(Sensor(self.center, self.back_left, 300, 7))
#       self.sensors.append(Sensor(self.center, self.back_right, 300, 8))
        
        
        self.score = 0
        self.score_label = pyglet.text.Label(('Score: ' + str(self.score)), font_name='Times New Roman', font_size=20, x=920, y=970)
        
        self.neuralnetwork = NeuralNetwork()
        self.tezine1 = np.empty([INPUT_SIZE, HIDDEN1_LAYER_SIZE])
        self.tezine2 = np.empty([HIDDEN1_LAYER_SIZE, HIDDEN2_LAYER_SIZE])
        self.tezine3 = np.empty([HIDDEN2_LAYER_SIZE, OUTPUT_SIZE])
        
    def on_crash(self):    
        self.posx = self.init_posx
        self.posy = self.init_posy
        self.sprite.rotation = self.init_rotation
        self.vel = 0
        self.score = 0
        
    def drive_with_network(self):
        sensor_input = np.empty((1, INPUT_SIZE))
        for i in range(5):      #5 senzora
            sensor_input[0][i] = self.sensors[i].distance/self.sensors[i].max_length
        
        out = self.neuralnetwork.calc_output(sensor_input, self.tezine1, self.tezine2, self.tezine3)

        if(out[0][0] <= 0.2):
            self.key_left = True
            self.key_right = False
            self.rot_val = 3
        if(out[0][0] > 0.2 and out[0][0] <= 0.4):
            self.key_left = True
            self.key_right = False
            self.rot_val = 1.5
        if(out[0][0] > 0.4 and out[0][0] <= 0.6):
            self.key_left = False
            self.key_right = False
        if(out[0][0] > 0.6 and out[0][0] <= 0.8):
            self.key_left = False
            self.key_right = True
            self.rot_val = 1.5
        if (out[0][0] > 0.8):
            self.key_left = False
            self.key_right = True
            self.rot_val = 3


        if (out[0][1] < 0.2):
            self.key_up = False
            self.key_down = True
        if (out[0][1] >= 0.2):
            self.key_up = True
            self.key_down = False
            

    
#    def draw_car_vertices(self):
#        pyglet.graphics.draw(6, pyglet.gl.GL_POINTS,
#                             ('v2f', (self.front.x, self.front.y, 
#                                      self.front_left.x, self.front_left.y, 
#                                      self.front_right.x, self.front_right.y, 
#                                      self.back.x, self.back.y, 
#                                      self.back_right.x, self.back_right.y, 
#                                      self.back_left.x, self.back_left.y, 
#                                      #self.front_left_middle.x, self.front_left_middle.y, 
#                                      #self.front_right_middle.x, self.front_right_middle.y
#                                      )))
    
    def draw_car_edges(self):
        if self.crash:
            pyglet.graphics.draw(8, pyglet.gl.GL_LINES,
                                     ('v2f', (self.front_left.x, self.front_left.y, self.front_right.x, self.front_right.y, 
                                              self.front_right.x, self.front_right.y, self.back_right.x, self.back_right.y, 
                                              self.back_left.x, self.back_left.y, self.back_right.x, self.back_right.y, 
                                              self.front_left.x, self.front_left.y, self.back_left.x, self.back_left.y)), 
                                    ('c3B', (255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0)))
                                     
        if self.reward:
            pyglet.graphics.draw(8, pyglet.gl.GL_LINES,
                                     ('v2f', (self.front_left.x, self.front_left.y, self.front_right.x, self.front_right.y, 
                                              self.front_right.x, self.front_right.y, self.back_right.x, self.back_right.y, 
                                              self.back_left.x, self.back_left.y, self.back_right.x, self.back_right.y, 
                                              self.front_left.x, self.front_left.y, self.back_left.x, self.back_left.y)), 
                                    ('c3B', (0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0)))
     
         
    def draw(self):
        self.sprite.draw()
        #self.draw_car_vertices()
        for sensor in self.sensors:
            sensor.draw()
        self.draw_car_edges()
        self.score_label.draw()

    def update(self, dt):
        if self.car_ready:
            self.drive_with_network()
                
        if self.key_up:
            self.vel += self.acc
            if self.vel >= self.max_vel:
                self.vel = self.max_vel

        if self.key_down:
            self.vel -= self.acc
            if self.vel <= self.min_vel:
                self.vel = self.min_vel
            
        if self.key_right:
            if self.vel <= 30:
                self.sprite.rotation += abs(self.vel)*((self.max_rotation/self.max_vel)+0.125)
            else:
                self.sprite.rotation += self.rot_val + abs(self.vel)*((self.max_rotation/self.max_vel))

        if self.key_left:
            if self.vel <= 30:
                self.sprite.rotation -= abs(self.vel)*((self.max_rotation/self.max_vel)+0.125)
            else:
                self.sprite.rotation -= self.rot_val + abs(self.vel)*((self.max_rotation/self.max_vel))
                
        self.sprite.rotation %= 360
        
        self.posx += self.vel * dt * np.cos(np.radians(self.sprite.rotation))
        self.posy += self.vel * dt * np.sin(np.radians(self.sprite.rotation))*(-1)
        
                
        """
        *Ovdje izračunao sinA, cosA, sinB, cosB prije i onda samo zvao vrijednosti,
            to će smanjit korištenje cos i sin funkcija koje su sporije
        *Nemoram računat kut za jednu i dugu stranu(180 stupnjeva), 
            samo promjenim predznake vrijednosti sinusa i kosinusa
        """
        
        #car position
        self.sprite.x = self.posx
        self.sprite.y = self.posy
        
        #car vertices
        tmp_cosA = np.cos(np.radians(self.sprite.rotation))
        tmp_sinA = np.sin(np.radians(self.sprite.rotation))
        
        self.center.x = self.posx + 0.25*self.width*tmp_cosA
        self.center.y = self.posy + 0.25*self.width*tmp_sinA*(-1)
        
        self.front.x = self.posx + 0.75*self.width*tmp_cosA
        self.front.y = self.posy + 0.75*self.width*tmp_sinA*(-1)
        
        self.back.x = self.posx + 0.25*self.width*tmp_cosA*(-1)
        self.back.y = self.posy + 0.25*self.width*tmp_sinA
        
        dy = (self.front.y-self.posy)*(-1)
        dx = self.front.x-self.posx
        
        if(np.abs(dy) < EPSILON):
            beta_angle = np.degrees(np.arctan(dx/EPSILON))*(-1)
        else:
            beta_angle = np.degrees(np.arctan(dx/dy))*(-1)
        
        if dy < 0:
            beta_angle += 180
            
        tmp_sinB = np.sin(np.radians(beta_angle))
        tmp_cosB = np.cos(np.radians(beta_angle))
        
        self.left.x = self.center.x + 0.5*self.height*tmp_cosB
        self.left.y = self.center.y + 0.5*self.height*tmp_sinB*(-1)
        
        self.right.x = self.center.x + 0.5*self.height*tmp_cosB*(-1)
        self.right.y = self.center.y + 0.5*self.height*tmp_sinB
        
        self.front_left.x = self.front.x + 0.5*self.height*tmp_cosB
        self.front_left.y = self.front.y + 0.5*self.height*tmp_sinB*(-1)
        
        self.front_right.x = self.front.x + 0.5*self.height*tmp_cosB*(-1)
        self.front_right.y = self.front.y + 0.5*self.height*tmp_sinB
        
        self.back_left.x = self.back.x + 0.5*self.height*tmp_cosB
        self.back_left.y = self.back.y + 0.5*self.height*tmp_sinB*(-1)
        
        self.back_right.x = self.back.x + 0.5*self.height*tmp_cosB*(-1)
        self.back_right.y = self.back.y + 0.5*self.height*tmp_sinB
        
        for sensor in self.sensors:
            sensor.update()
        
        