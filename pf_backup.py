import random, pygame, math

def diffuse(self):
    if not hasattr(self,'diffusion_rate'): self.diffusion_rate = 0.5
    self.x += (random.random()-0.5)*self.diffusion_rate
    self.y += (random.random()-0.5)*self.diffusion_rate

def draw_as_point(self, s):
    pygame.draw.rect(s, self.color, (self.x,self.y,1,1))

def attract_repel(self):

    distance = math.sqrt( (self.x-self.target.x)**2 + (self.y-self.target.y)**2 )
    direction = math.atan2( self.target.y-self.y, self.target.x-self.x )
    if distance > 10:
        self.x += math.cos(direction) * 3
        self.y += math.sin(direction) * 3
    elif distance < 5:
        self.x -= math.cos(direction) * 1
        self.y -= math.sin(direction) * 1

    for o in self.others:
        if o == self.target: continue
        if o == self: continue
        distance = math.sqrt( (self.x-o.x)**2 + (self.y-o.y)**2 )
        direction = math.atan2( o.y-self.y, o.x-self.x )
        if distance < 20:
            self.x -= math.cos(direction) * 1
            self.y -= math.sin(direction) * 1

def draw_to_target(self,s):
    pygame.draw.line(s, self.color, (self.x, self.y), (self.target.x, self.target.y))