import pygame
from random import random

r=4 # Particle size
unit = 150 # Pixels per grid unit
vunit = 0.005 # Initial velocity bound
G=0.0000005 # Strength of gravity
nbody=50 # Number of bodies to initialize
r2floor = 0.01 # 1/r2floor is bound on inverse square to limit accelerations
draw_bary = False # Draw center of mass? TODO: doesn't work
mouse_m = 100 # Mass of particles created by click
default_m = 1 # Mass of initialized particles
screen_size = 640 # Dimensions of window
screen_boundary = True # Bounce off walls?
wall_damp = 1 # Velocity after wall bounce = -wall_damp * Velocity before wall bounce. Simulates losing energy in collision
collide_particles = False # Have particles bounce off each other? TODO: Elastic collisions?

class Body:
    def __init__(self, m, x, y, vx, vy, isMouse=False):
        self.m = m
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.isMouse = isMouse

def cartesian_to_screen(x,y,unit):
    return (screen_size/2 + x*unit, screen_size/2-y*unit)

def screen_to_cartesian(x,y,unit):
    return ((x-screen_size/2)/unit, (screen_size/2-y)/unit)

def rand_range(low, high):
    return random() * (high-low) + low

bodies = [Body(default_m, rand_range(-1,1), rand_range(-1,1), rand_range(-vunit,vunit),rand_range(-vunit,vunit)) for i in range(nbody)]

pygame.init()
screen = pygame.display.set_mode((640,640))
pygame.display.set_caption('GravitySim')
running = True

while running:
    pos = pygame.mouse.get_pos()
    mouse_v = pygame.mouse.get_rel()

    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            cart = screen_to_cartesian(pos[0],pos[1],unit)
            bodies.append(Body(mouse_m,cart[0],cart[1],0,0))

    for body in sorted(bodies, key=lambda b: b.m, reverse=True): # Draw most massive underneath less massive
        pygame.draw.circle(screen, # Draw to screen
                           (0,0,0) if body.m <= default_m else (0,0,255), # Color based on mass
                           cartesian_to_screen(body.x,body.y,unit), # Convert space coordinates to pixel coordinates
                           ((body.m/3.14159)**0.5)*r) # Make circle area proportional to mass

        if screen_boundary:
            x,y = cartesian_to_screen(body.x,body.y,unit)
            if x > screen_size or x < 0:
                body.vx *= -wall_damp
            if y > screen_size or y < 0:
                body.vy *= -wall_damp

        for other in bodies:
            if other != body:
                dx = body.x - other.x
                dy = body.y - other.y
                r2 = max(dx ** 2 + dy ** 2, r2floor) # Change r2floor to body.m/3.14159 have r2 correspond to the actual radius of the body

                body.vx -= (G * other.m / r2) * (dx / (r2 ** 0.5))
                body.vy -= (G * other.m / r2) * (dy / (r2 ** 0.5))

    xbar = 0
    ybar = 0

    for body in bodies:
        body.x += body.vx
        body.y += body.vy
        xbar += body.x # TODO: Take particle masses into account when weighting the average
        ybar += body.y

    nbody = len(bodies)

    try:
        xbar /= nbody
        ybar /= nbody
    except:
        pass

    if draw_bary:
        pygame.draw.circle(screen, (255,0,0), cartesian_to_screen(xbar,ybar,unit),2*r)

    pygame.display.update()