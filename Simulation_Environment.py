import pygame, sys, copy
import key_input as IN
import particle, random
import particle_functions
import draw_vars

def num_to_bin(n, num_bits): return ('{0:0'+str(num_bits)+'b}').format(n)
def bin_to_num(n): return int(n,2)

pygame.init()
width = height = 500
s = pygame.display.set_mode((width,height))
p_clock = pygame.time.Clock()

# Set the rule to be examined.l
rule = num_to_bin(110, 8)
particle_length = 3
string_length = 6

str_succ = {}
for sr in range(0,2**string_length):
    string = num_to_bin(sr, string_length)
    particles = []
    for x in range(len(string)):
        particles.append((string * 2)[x:x + particle_length])
    result = []
    for p in particles:
        result.append(rule[bin_to_num(p)])
    str_succ[string] = "".join(result)

reified_actors = []
for key in str_succ:
    temp = particle.particle(
        width/2+(random.random()-0.5)*width/1.5,
        height/2+(random.random()-0.5)*height/1.5)
    temp.update_functions.append( particle_functions.diffuse )
    temp.draw_functions.append(particle_functions.draw_as_point)
    temp.draw_functions.append( particle_functions.draw_selected)
    temp.name = key
    reified_actors.append(temp)

for re in reified_actors:
    target = None
    for re2 in reified_actors:
        if re2.name == str_succ[re.name]:
            target = re2
            continue
    re.update_functions.append( particle_functions.attract_repel )
    re.draw_functions.append( particle_functions.draw_to_target )
    re.others = reified_actors
    re.target = target

paused = False
smallest = None
while True:

    # Update input state(s).
    IN.last_keys_down = copy.deepcopy(IN.keys_down)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN: IN.keys_down[str(event.key)] = True
        elif event.type == pygame.KEYUP: IN.keys_down[str(event.key)] = False
        elif event.type == pygame.MOUSEBUTTONUP: IN.keys_down[str(event.button)] = False
        elif event.type == pygame.MOUSEBUTTONDOWN: IN.keys_down[str(event.button)] = True
        elif event.type == pygame.MOUSEMOTION: IN.mouse_position = event.pos

    pygame.draw.rect(s,(20,20,20),(0,0,width,height))

    if IN.down( pygame.K_UP ):
        draw_vars.y_shift += 6
    if IN.down( pygame.K_DOWN ):
        draw_vars.y_shift -= 6
    if IN.down( pygame.K_LEFT):
        draw_vars.x_shift += 6
    if IN.down( pygame.K_RIGHT):
        draw_vars.x_shift -= 6

    if IN.pressed(pygame.K_SPACE): paused = not paused

    if IN.pressed( '1' ): # Mouse button 1
        # Find the actor closest to where I clicked.
        smallest_dist = 9999
        smallest = None
        for re in reified_actors:
            distance_sq = (IN.mouse_position[0]-draw_vars.x_shift-re.x)**2+(IN.mouse_position[1]-draw_vars.y_shift-re.y)**2
            if (distance_sq > 200): continue
            if distance_sq < smallest_dist:
                smallest_dist = distance_sq
                smallest = re
        if smallest is not None: smallest.selected = True
        #print("selected", smallest)
        for re in reified_actors:
            if re != smallest: re.selected = False

    if IN.down( '1' ):
        if smallest != None:
            smallest.x = -draw_vars.x_shift + IN.mouse_position[0]
            smallest.y = -draw_vars.y_shift + IN.mouse_position[1]

    if IN.pressed( pygame.K_EQUALS ) or IN.down( pygame.K_0): # Move on to the next reified number.
        if smallest != None:
            next_num = num_to_bin((bin_to_num(smallest.name) + 1) % 2**string_length, string_length)
            for re in reified_actors:
                re.selected = re.name == next_num
                if re.selected: smallest = re

    if IN.pressed( pygame.K_MINUS ) or IN.down( pygame.K_9 ): # Move on to the next reified number.
        if smallest != None:
            k = (bin_to_num(smallest.name) + -1)
            k += 0 if k >= 0 else 2**string_length-1
            next_num = num_to_bin(k, string_length)
            for re in reified_actors:
                re.selected = re.name == next_num
                if re.selected: smallest = re

    if IN.down(pygame.K_q):
        for re in reified_actors:
            re.x = (re.x-width/2)/1.02 + width/2
            re.y = (re.y-height/2)/1.02 + height/2

    if not paused:
        for p in reified_actors:
            p.update()
    for p in reified_actors:
        p.draw(s)

    basicfont = pygame.font.SysFont("Deja Vu Sans",12)
    text = basicfont.render("Rule " + str(bin_to_num(rule)) + " (" + rule + ") over the space of " + str(string_length) +"-bit binary lattices",True, (255,255,255))
    s.blit(text, (width/2-200, height-50, 200, 100))

    if smallest != None:
        text = basicfont.render("Selected: "+str(bin_to_num(smallest.name))+"/"+str(2**string_length-1)+" ("+smallest.name+")",True, (255,255,255))
        s.blit(text, (20, 20, 200, 100))
    else:
        text = basicfont.render("[No node selected]",True, (255,255,255))
        s.blit(text, (20, 20, 200, 100))

    pygame.display.flip()
    p_clock.tick(60)