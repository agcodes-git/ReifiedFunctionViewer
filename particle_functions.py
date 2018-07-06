# TODO: Controls for structures
# way to color separate structures
# way to grab structures
# way to zoom
# way to move about
# auto zoom
# auto-moving
# auto-scaling
import key_input as IN

import draw_vars
import random, pygame, math

def diffuse(self):
    if not hasattr(self,'diffusion_rate'): self.diffusion_rate = 1
    self.x += (random.random()-0.5)*self.diffusion_rate
    self.y += (random.random()-0.5)*self.diffusion_rate

def draw_as_point(self, s):
    pygame.draw.rect(s, self.color, (self.x-3,self.y-3,6,6))

def attract_repel(self):

    dist_const = 10

    if self.target != self:
        distance = math.sqrt( (self.x-self.target.x)**2 + (self.y-self.target.y)**2 )
        direction = math.atan2( self.target.y-self.y, self.target.x-self.x )
        if distance > dist_const*2:
            self.x += math.cos(direction) * 2
            self.y += math.sin(direction) * 2
        elif distance < dist_const:
            self.x -= math.cos(direction) * 1
            self.y -= math.sin(direction) * 1

    for o in self.others:
        if o == self.target: continue
        if o == self: continue
        #if self == o.target: continue
        distance = math.sqrt( (self.x-o.x)**2 + (self.y-o.y)**2 )
        direction = math.atan2( o.y-self.y, o.x-self.x )
        if distance < dist_const*4:
            self.x -= math.cos(direction) * 1
            self.y -= math.sin(direction) * 1

def draw_to_target(self,s):
    if self.target == self: return
    pygame.draw.line(s, self.color, (self.x, self.y), (self.target.x+draw_vars.x_shift, self.target.y+draw_vars.y_shift),2)
    if random.random() > 0.5: self.target.color = self.color
    else: self.color = self.target.color

def draw_selected(self,s):
    if not hasattr(self, 'selected'): return
    if self.selected:
        pygame.draw.ellipse(s, (255,255,255), (self.x-10, self.y-10, 20, 20), 1)
        basicfont = pygame.font.SysFont("Times New Roman",20)
        text = basicfont.render(self.name,True, (255,255,255))
        s.blit(text, (self.x+15,self.y-10,100,20))