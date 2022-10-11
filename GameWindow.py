from __future__ import division
import pyglet
import numpy as np
from pyglet.window import key, mouse
from GameVehicles import Car, preload_image
from GameStage import Stage
from GameGeometry import Point, LineSegment, do_lines_intersect, segment_intersect, distance_between_two_points
from GeneticAlgorithm import Population, POP_SIZE, Chromosome
from LoadAgents import vrni_agenta

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(100, 0)
        self.fps = 40
        self.frame_rate = 1/self.fps
        
        
        self.stage = Stage()
        self.line_order = 0
        
        self.timeout_counter = 0
        self.timeout_time = 3
        
        self.population = Population(POP_SIZE)
        
        self.agent1 = Chromosome()
        self.agent1.genes = vrni_agenta(1)
        self.agent1.update_weights()
        
        self.agent2 = Chromosome()
        self.agent2.genes = vrni_agenta(2)
        self.agent2.update_weights()
        
        self.agent3 = Chromosome()
        self.agent3.genes = vrni_agenta(3)
        
        self.agent4 = Chromosome()
        self.agent4.genes = vrni_agenta(4)
        
        self.agent5 = Chromosome()
        self.agent5.genes = vrni_agenta(5)
        
        np.copyto(self.population.chromosomes[0].genes, self.agent1.genes)
        np.copyto(self.population.chromosomes[1].genes, self.agent2.genes)
        np.copyto(self.population.chromosomes[2].genes, self.agent3.genes)
        np.copyto(self.population.chromosomes[3].genes, self.agent4.genes)
        np.copyto(self.population.chromosomes[4].genes, self.agent5.genes)
        
        self.pop_iterator = POP_SIZE
        self.pop_step = 0
        
        self.decision_pointer = 0

############################################################################################################################################
        """
        //PYGLET varijable\\
        """
############################################################################################################################################

        car_sprite = pyglet.sprite.Sprite(preload_image('car.png'))
        self.player = Car(car_sprite)
    
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)                                            # transparency
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)   # transparency
        
        #lines
        self.stat_lines = pyglet.graphics.vertex_list(8, ('v2i', (300, 0, 300, 1000, 900, 950, 900, 1000, 900, 950, 1050, 950, 1050, 950, 1050, 1000)))
        
        #quads
        self.decision_box = pyglet.graphics.vertex_list(4, ('v2i', (10, 595, 10, 620, 250, 620, 250, 595)), ('c4B', (255, 255, 255, 100)*4))
        
        #labels
        self.timer_label = pyglet.text.Label(("Timeout timer: " + str(self.timeout_time)), 
                          font_name='Times New Roman', 
                          color = (255, 255, 255, 200),
                          font_size=20,
                          x=30, y=960)
        self.best_fitness_label = pyglet.text.Label(("Best Fitness: " + str(self.population.Best_fitness)), 
                          font_name='Times New Roman', 
                          color = (255, 255, 255, 255),
                          font_size=20,
                          x=30, y=900)
        self.cross_label = pyglet.text.Label(('Crossover probability: ' + str(self.population.CROSSOVER_PROBABILITY)), 
                          font_name='Times New Roman', 
                          color = (255, 255, 255, 255),
                          font_size=15,
                          x=15, y=600)
        self.mut_label = pyglet.text.Label(('Mutation probability: ' + str(self.population.MUTATION_PROBABILITY)), 
                          font_name='Times New Roman', 
                          color = (255, 255, 255, 255),
                          font_size=15,
                          x=15, y=570)
        self.elite_label = pyglet.text.Label(('Elite: ' + str(self.population.ELITE_NUM)), 
                          font_name='Times New Roman', 
                          color = (255, 255, 255, 255),
                          font_size=15,
                          x=15, y=540)
        self.kick_label = pyglet.text.Label(('Kick: ' + str(self.population.KICK_NUM)), 
                          font_name='Times New Roman', 
                          color = (255, 255, 255, 255),
                          font_size=15,
                          x=15, y=510)
        self.maxvel_label = pyglet.text.Label(('MAX velocity: ' + str(self.player.max_vel)), 
                          font_name='Times New Roman', 
                          color = (255, 255, 255, 255),
                          font_size=15,
                          x=15, y=480)
        
        
        
###############################################################################################################################################
    """
    //Funkcije za rukovanje ulazima\\
    """
###############################################################################################################################################
    
    def on_key_press(self, symbol, modifires):   
        if self.pop_iterator < 47 or self.pop_iterator == 50:
            if symbol == key.UP:
                if(self.decision_pointer == 0):
                    self.decision_pointer = 4
                else:
                    self.decision_pointer -= 1
            if symbol == key.DOWN:
                if(self.decision_pointer == 4):
                    self.decision_pointer = 0
                else:
                    self.decision_pointer += 1
            if symbol == key.LEFT:
                if self.decision_pointer == 0:
                    if self.population.CROSSOVER_PROBABILITY > 0.1:
                        self.population.CROSSOVER_PROBABILITY -= 0.01
                if self.decision_pointer == 1:
                    if self.population.MUTATION_PROBABILITY > 0.02:
                        self.population.MUTATION_PROBABILITY -= 0.01
                if self.decision_pointer == 2:
                    if self.population.ELITE_NUM > 2:
                        self.population.ELITE_NUM -= 1
                if self.decision_pointer == 3:
                    if self.population.KICK_NUM > 2:
                        self.population.KICK_NUM -= 2
                if self.decision_pointer == 4:
                    if self.player.max_vel > 100:
                        self.player.max_vel -= 5
            if symbol == key.RIGHT:
                if self.decision_pointer == 0:
                    if self.population.CROSSOVER_PROBABILITY < 0.9:
                        self.population.CROSSOVER_PROBABILITY += 0.01
                if self.decision_pointer == 1:
                    if self.population.MUTATION_PROBABILITY < 0.5:
                        self.population.MUTATION_PROBABILITY += 0.01
                if self.decision_pointer == 2:
                    if self.population.ELITE_NUM < 10:
                        self.population.ELITE_NUM += 1
                if self.decision_pointer == 3:
                    if self.population.KICK_NUM < 40:
                        self.population.KICK_NUM += 2
                if self.decision_pointer == 4:
                    if self.player.max_vel < 350:
                        self.player.max_vel += 5
            
        if self.player.car_ready:
            if symbol == key.W:
                self.player.key_up = True
            if symbol == key.S:
                self.player.key_down = True
            if symbol == key.A:
                self.player.key_left = True
            if symbol == key.D:
                self.player.key_right = True
            if symbol == key.SPACE:
                if self.player.crash:
                    self.player.on_crash()
                    self.player.crash = False
                    self.stage.open_reward = 0
                    self.stage.lap_counter = 0
                    self.timeout_time = 5
            if symbol == key.ENTER:
                pass
                
            
    def on_key_release(self, symbol, modifires):
        if self.player.car_ready:
            if symbol == key.RIGHT:
                self.player.key_right = False
            if symbol == key.LEFT:
                self.player.key_left = False
            if symbol == key.UP:
                self.player.key_up = False
            if symbol == key.DOWN:
                self.player.key_down = False
#            if symbol == key.SPACE:
#                self.player.key_space = False
                  
    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            if self.line_order == 0:
                self.stage.add_vertex(x, y, 1)
            if self.line_order == 1:
                self.stage.add_vertex(x, y, 2)
            if self.line_order == 2:
                self.stage.add_vertex(x, y, 3)
            if self.line_order == 3:
                self.player.init_posx = x
                self.player.init_posy = y
                self.player.posx = x
                self.player.posy = y
                self.player.car_placed = True
                
        if button == mouse.MIDDLE:
            if self.line_order < 5:
                self.line_order += 1
                if self.line_order >= 4:
                    self.player.car_ready = True
                    np.copyto(self.player.tezine1, self.agent1.weights1)
                    np.copyto(self.player.tezine2, self.agent1.weights2)
                    np.copyto(self.player.tezine3, self.agent1.weights3)

                
        if button == mouse.RIGHT:
            if self.line_order == 3:
                angle = np.degrees(np.arctan((y-self.player.posy)/(x-self.player.posx))) *(-1)
                if (x-self.player.posx) < 0:
                    angle += 180
                self.player.init_rotation = angle
                self.player.sprite.rotation = angle
                
###############################################################################################################################################
    """
    //Funkcije za kolizije\\
    """
###############################################################################################################################################  
    
    def car_track_collision(self):
        stage_point1 = Point()
        stage_point2 = Point()
        stage_line = LineSegment(stage_point1, stage_point2)
        
        #linija 1
        for i in range(self.stage.line1_len):
            if i == self.stage.line1_len-1:
                stage_point1.x = self.stage.line1[2*i]
                stage_point1.y = self.stage.line1[2*i+1]
                stage_point2.x = self.stage.line1[0]
                stage_point2.y = self.stage.line1[1]
            else:
                stage_point1.x = self.stage.line1[2*i]
                stage_point1.y = self.stage.line1[2*i+1]
                stage_point2.x = self.stage.line1[2*(i+1)]
                stage_point2.y = self.stage.line1[2*(i+1)+1]
                
            if (do_lines_intersect(self.player.front_line, stage_line) or
                do_lines_intersect(self.player.right_line, stage_line) or
                do_lines_intersect(self.player.back_line, stage_line) or
                do_lines_intersect(self.player.left_line, stage_line)):
                self.player.crash = True
                break
        
        #linija 2
        if not self.player.crash:
            for i in range(self.stage.line2_len):
                if i == self.stage.line2_len-1:
                    stage_point1.x = self.stage.line2[2*i]
                    stage_point1.y = self.stage.line2[2*i+1]
                    stage_point2.x = self.stage.line2[0]
                    stage_point2.y = self.stage.line2[1]
                else:
                    stage_point1.x = self.stage.line2[2*i]
                    stage_point1.y = self.stage.line2[2*i+1]
                    stage_point2.x = self.stage.line2[2*(i+1)]
                    stage_point2.y = self.stage.line2[2*(i+1)+1]
                    
                if (do_lines_intersect(self.player.front_line, stage_line) or
                    do_lines_intersect(self.player.right_line, stage_line) or
                    do_lines_intersect(self.player.back_line, stage_line) or
                    do_lines_intersect(self.player.left_line, stage_line)):
                    self.player.crash = True
                    break

        del stage_line, stage_point1, stage_point2
                    
    def sensor_track_collision(self):
        intersection = Point()
        stage_point1 = Point()
        stage_point2 = Point()
        stage_line = LineSegment(stage_point1, stage_point2)
        
        for sensor in self.player.sensors:
            tmp_ray_len = sensor.max_length
            b1 = np.array([sensor.sensor_ray.a.x, sensor.sensor_ray.a.y])
            b2 = np.array([sensor.sensor_ray.b.x, sensor.sensor_ray.b.y])
            
            for i in range(self.stage.line1_len):
                if i == self.stage.line1_len-1:
                    stage_point1.x = self.stage.line1[2*i]
                    stage_point1.y = self.stage.line1[2*i+1]
                    stage_point2.x = self.stage.line1[0]
                    stage_point2.y = self.stage.line1[1]
                else:
                    stage_point1.x = self.stage.line1[2*i]
                    stage_point1.y = self.stage.line1[2*i+1]
                    stage_point2.x = self.stage.line1[2*(i+1)]
                    stage_point2.y = self.stage.line1[2*(i+1)+1]
                    
                if (do_lines_intersect(sensor.sensor_ray, stage_line)):
                    a1 = np.array([stage_line.a.x, stage_line.a.y])
                    a2 = np.array([stage_line.b.x, stage_line.b.y])
                    inters = segment_intersect(a1, a2, b1, b2)
                    del a1, a2
                    intersection.x = inters[0]
                    intersection.y = inters[1]
                    dist = distance_between_two_points(intersection, sensor.sensor_ray.a)
                    tmp_ray_len = np.minimum(tmp_ray_len, dist)
            
            for i in range(self.stage.line2_len):
                if i == self.stage.line2_len-1:
                    stage_point1.x = self.stage.line2[2*i]
                    stage_point1.y = self.stage.line2[2*i+1]
                    stage_point2.x = self.stage.line2[0]
                    stage_point2.y = self.stage.line2[1]
                else:
                    stage_point1.x = self.stage.line2[2*i]
                    stage_point1.y = self.stage.line2[2*i+1]
                    stage_point2.x = self.stage.line2[2*(i+1)]
                    stage_point2.y = self.stage.line2[2*(i+1)+1]
                    
                if (do_lines_intersect(sensor.sensor_ray, stage_line)):
                    a1 = np.array([stage_line.a.x, stage_line.a.y])
                    a2 = np.array([stage_line.b.x, stage_line.b.y])
                    inters = segment_intersect(a1, a2, b1, b2)
                    del a1, a2
                    intersection.x = inters[0]
                    intersection.y = inters[1]
                    dist = distance_between_two_points(intersection, sensor.sensor_ray.a)
                    tmp_ray_len = np.minimum(tmp_ray_len, dist)
            del b1, b2
            sensor.distance = tmp_ray_len     
        del intersection, stage_point1, stage_point2, stage_line
        
    def car_reward_collision(self):
        reward_point1 = Point()
        reward_point2 = Point()
        reward_line = LineSegment(reward_point1, reward_point2)
        
        for i in range(self.stage.reward_len//2):
            if i == self.stage.open_reward:
                reward_point1.x = self.stage.reward_list[4*i]
                reward_point1.y = self.stage.reward_list[4*i+1]
                reward_point2.x = self.stage.reward_list[4*i+2]
                reward_point2.y = self.stage.reward_list[4*i+3]
                
                if (do_lines_intersect(self.player.front_line, reward_line) or
                    do_lines_intersect(self.player.right_line, reward_line) or
                    do_lines_intersect(self.player.back_line, reward_line) or
                    do_lines_intersect(self.player.left_line, reward_line)):
                    self.player.reward = True
                    if self.stage.open_reward == (self.stage.reward_len//2)-1:
                        self.stage.lap_counter += 1
                    self.stage.open_reward += 1
                    self.stage.open_reward %= self.stage.reward_len//2
                    self.player.score += 1
                    self.timeout_time += 2
                    break
                else:
                    self.player.reward = False
        del reward_point1, reward_point2, reward_line
        
###############################################################################################################################################
    """
    //Funkcije za crtanje i update\\
    """
###############################################################################################################################################
    
    def timeout_timer(self):
        if self.player.car_ready:
            if self.timeout_counter >= self.fps:
                self.timeout_counter %= self.fps
                self.timeout_time -= 1
                self.timer_label.text = ("Timeout timer: " + str(self.timeout_time))
            else:
                self.timeout_counter += 1
            
            if self.timeout_time == 0:
                self.player.crash = True
                    
    def display_statistic(self):
        box_h = 595 - self.decision_pointer*30
        self.decision_box.vertices = [10, box_h, 10, box_h+25, 250, box_h+25, 250, box_h]
        self.cross_label.text = ('Crossover probability: ' + str(round(self.population.CROSSOVER_PROBABILITY, 2)))
        self.mut_label.text = ('Mutation probability: ' + str(round(self.population.MUTATION_PROBABILITY, 2)))
        self.elite_label.text = ('Elite: ' + str(self.population.ELITE_NUM))
        self.kick_label.text = ('Kick: ' + str(self.population.KICK_NUM))
        self.maxvel_label.text = ('MAX velocity: ' + str(self.player.max_vel))
        self.player.score_label.text = ('Score: ' + str(self.player.score))
        self.best_fitness_label.text = ("Best Fitness: " + str(self.population.Best_fitness))
        
        self.stat_lines.draw(pyglet.gl.GL_LINES)
        self.decision_box.draw(pyglet.gl.GL_QUADS)
        self.cross_label.draw()
        self.mut_label.draw()
        self.elite_label.draw()
        self.kick_label.draw()
        self.maxvel_label.draw()
        self.player.score_label.draw()
        self.best_fitness_label.draw()
        
    def on_draw(self):
        self.clear()
        self.display_statistic()
        self.timer_label.draw()
        self.stage.draw()
        if self.player.car_placed:
            self.player.draw()
        
            
    def update(self, dt):
        if self.player.crash == False:
            self.player.update(dt)
            self.car_track_collision()
            self.sensor_track_collision()
            self.car_reward_collision()
            self.timeout_timer()
            if self.stage.lap_counter == 3:
                self.player.score += 100
                self.player.crash = True
        else:
            if self.pop_iterator < POP_SIZE-1:
                self.population.chromosomes[self.pop_iterator].fitness = self.player.score
                print("score: " + str(self.population.chromosomes[self.pop_iterator].fitness))
                if(self.population.Best_fitness < self.population.chromosomes[self.pop_iterator].fitness):
                    self.population.Best_fitness = self.population.chromosomes[self.pop_iterator].fitness
                self.pop_iterator += 1
            else:
                self.population.make_a_step()
                print(self.population.chromosomes[0].genes)
                self.pop_iterator = 0
                self.pop_step += 1
                
            self.population.chromosomes[self.pop_iterator].update_weights()
            np.copyto(self.player.tezine1, self.population.chromosomes[self.pop_iterator].weights1)
            np.copyto(self.player.tezine2, self.population.chromosomes[self.pop_iterator].weights2)
            np.copyto(self.player.tezine3, self.population.chromosomes[self.pop_iterator].weights3)

            print("Step: " + str(self.pop_step) + ", iterator: " + str(self.pop_iterator))
            
            #reset igre
            self.player.on_crash()
            self.player.crash = False
            self.stage.open_reward = 0
            self.stage.lap_counter = 0
            self.timeout_time = 5

if __name__ == "__main__":
    window = Window(1700, 1000, "AI learns to drive")
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
    
