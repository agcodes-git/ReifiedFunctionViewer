import pygame, random, math, draw_vars, key_input as IN
class particle:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        r = random.random()
        g = random.random()
        b = random.random()
        n = math.sqrt(r*r+g*g+b*b)

        r /= n
        g /= n
        b /= n

        self.color = (r*255, g*255, b*255)
        self.draw_functions = []
        self.update_functions = []

    def update(self):
        for uf in self.update_functions: uf(self)

    def draw(self,s):

        # Recolor
        if IN.pressed(pygame.K_r):
            r = random.random()
            g = random.random()
            b = random.random()
            n = math.sqrt(r*r+g*g+b*b)

            r /= n
            g /= n
            b /= n

            self.color = (r*255, g*255, b*255)


        original_x = self.x
        original_y = self.y
        self.x += draw_vars.x_shift
        self.y += draw_vars.y_shift
        for df in self.draw_functions: df(self,s)
        self.x = original_x
        self.y = original_y

