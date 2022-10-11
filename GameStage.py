import pyglet

class Stage:
    def __init__(self):
        self.line1 = []
        self.line1_len = 0
        self.line2 = []
        self.line2_len = 0
        self.reward_list = []
        self.reward_len = 0
        
        self.open_reward = 0
        
        self.lap_counter = 0
        
        self.line1_ver = pyglet.graphics.vertex_list(self.line1_len, ('v2f', self.line1))
        self.line2_ver = pyglet.graphics.vertex_list(self.line2_len, ('v2f', self.line2))
        self.reward_ver = pyglet.graphics.vertex_list(self.reward_len, ('v2f', self.reward_list))
    
    def add_vertex(self, x, y, line_num):
        if line_num == 1:
            self.line1.append(x)
            self.line1.append(y)
            self.line1_len += 1
        if line_num == 2:
            self.line2.append(x)
            self.line2.append(y)
            self.line2_len += 1
        if line_num == 3:
            self.reward_list.append(x)
            self.reward_list.append(y)
            self.reward_len += 1
        
        self.line1_ver = pyglet.graphics.vertex_list(self.line1_len, ('v2f', self.line1))
        self.line2_ver = pyglet.graphics.vertex_list(self.line2_len, ('v2f', self.line2))
        self.reward_ver = pyglet.graphics.vertex_list(self.reward_len, ('v2f', self.reward_list), ('c4B', (0, 255, 0, 220)*self.reward_len))
        
    def draw(self):
        self.line1_ver.draw(pyglet.gl.GL_LINE_LOOP)
        self.line2_ver.draw(pyglet.gl.GL_LINE_LOOP)
        self.reward_ver.draw(pyglet.gl.GL_LINES)