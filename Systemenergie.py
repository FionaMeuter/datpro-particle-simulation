#Systemenergie

import math
import numpy as np

N = 10 # Anzahl der Teilchen
m = 1.0 # Masse eines Teilchens
q = 1.0 #Ladung des Teilchens
g = -10.0 # Gravitationskraft 
dt = 0.01 # Zeitschritte
steps = 10
y_min, y_max = 0, 100 # Höhe der Box
x_min, x_max = 0, 100 # Breite der Box

class Particle:
    def __init__(self, x, y, vx, vy): #Initiallisierung von Teilchen mit Position, Geschwindigkeit und Masse
        self.x = x #Position
        self.y = y #Geschwindigkeit
        self. vx = vx
        self.vy = vy 
    
    def move(self, timestep, box_size): #Position des Teilchen beruhend auf Geschwindigkeit und Zeit
        self.position = [
            self.position[i] + self.velocity [i]* timestep
            for i in range(len(self.position))
            ]

def systemenergie(particles):
    total_energie = 0.0
    for i, p in enumerate(particles):
        total_energie += m * g * p.y  #Gravitation
        v2 = p.vx**2 + p.vy**2
        total_energie += 0.5 * m * v2 #kinetische Energie
        for j in range(i+1, len(particles)):
            q = particles[j]
            dx = p.x - q.x
            dy = p.y - q.y
            r = math.sqrt(dx*dx + dy*dy)
            if r > 1e-12:
                total_energie += 0.5 * q**2 / r
    return total_energie
        

particles = [
    Particle(1.0, 45.0, 10.0, 0.0),
    Particle(99.0, 55.0, -10.0, 0.0),
    Particle(10.0, 50.0, 15.0, -15.0),
    Particle(20.0, 30.0, -15.0, -15.0),
    Particle(80.0, 70.0, 15.0, 15.0),
    Particle(80.0, 60.0, 15.0, 15.0),
    Particle(80.0, 50.0, 15.0, 15.0)
    ]

E = systemenergie(particles)
print("Energie", E)