#Teilchen definiert in Klasse

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation

class Particle:
    def __init__(self, position, velocity, mass): #Initiallisierung von Teilchen mit Position, Geschwindigkeit und Masse
        self.position = position #Position
        self.velocity = velocity #Geschwindigkeit
        self.mass = mass #Masse
    
    def move(self, timestep, box_size): #Position des Teilchen beruhend auf Geschwindigkeit und Zeit
        self.position = [
            self.position[i] + self.velocity [i]* timestep
            for i in range(len(self.position))
        ]
    def check_boundary(self, box_size):
        for i in range(len(self.position)):
            if self.position[i] < 0 or self.position[i] > box_size[i]:
                self.velocity[i] *= -1


#Beispielsimulation Teilchen in 2D Box für Boxgrenzen            
box_size = [10, 10]
dt = 0.1
timestep = 10
mass=1.0

position=[5, 5]
velocity=[25, 2]

#Plot vorbereiten
fig, ax = plt.subplots()
ax.set_xlim(0, box_size[0])
ax.set_ylim(0, box_size[1])
ax.set_aspect('equal')

#Rechteck Box zeichnen
rect = Rectangle((0,0), box_size[0], box_size[1], fill=False)
ax.add_patch(rect) 

#Punkt für Teilchen
point, = ax.plot([], [], 'ro', markersize=8)

def update(frame):
    position[0] += velocity[0] * dt
    position[1] += velocity[1] * dt
    point.set_data([position[0]], [position[1]])
    return point,

#Animation
ani = FuncAnimation(fig, update, frames=timestep, interval=50, blit=True)
plt.show()