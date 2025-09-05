#Hauptprogramm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#Konstanten
N = 10 # Anzahl der Teilchen
m = 1.0 # Masse eines Teilchens
q = 1.0 #Ladung des Teilchens
g = -10.0 # Gravitationskraft 
dt = 0.01 # Zeitschritte
steps = 10
y_min, y_max = 0, 100 # Höhe der Box
x_min, x_max = 0, 100 # Breite der Box


#Klasse der Teilchen
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
        

#Ableitung Statevektor berechnen
def f(s, m, q, g, positions):
    x, y, vx, vy = s #Position und Geschwindigkeit
    ax, ay = -10.0, g #Gravitation in y-Richtung
    
    for pos in positions: #Liste aller Teilchen
        dx = x - pos[0] #Abstandskomponente zu anderen Teilchen
        dy = y - pos[1]
        r3 = (dx**2 + dy**2)**1.5 #Nenner für Coulombkraft
        if r3 != 0:
            ax -= q**2 / m * dx / r3
            ay -= q**2 / m * dy / r3
            
    return np.array([vx, vy, ax, ay]) 

#Position und Geschwindigkeit nach Zeitschritt approximiert
def rk4_step(s, dt, m, q, g, positions):
    k1 = dt * f(s, m, q, g, positions)
    k2 = dt * f(s + 0.5*k1, m, q, g, positions)
    k3 = dt * f(s + 0.5*k2, m, q, g, positions)
    k4 = dt * f(s + k3, m, q, g, positions)
    return s + (k1 + 2*k2 + 2*k3 + k4) / 6


#Reflexion an Boxgrenzen
def reflect_particle(s, dt, m, q, g, positions):
    s_neu = rk4_step(s, dt, m, q, g, positions)
    
    if s_neu[0] < x_min or s_neu[0] > x_max:
        wall_x = x_min if s_neu[0] < x_min else x_max
        alpha = (wall_x - s[0]) / (s_neu[0] - s[0]) #Zeitschritt bis zur Wand
        s_wall = rk4_step(s, alpha*dt, m, q, g, positions)
        s_wall[2] = -s_wall[2] #Geschwinigkeit umdrehen
        s_neu = rk4_step(s_wall, (1-alpha)*dt, m, q, g, positions)
        
    if s_neu[1] < y_min or s_neu[1] > y_max:
        wall_y = y_min if s_neu [1] < y_min else y_max
        alpha = (wall_y - s[1]) / (s_neu[1] - s[1])
        s_wall = rk4_step(s, alpha*dt, m, q, g, positions)
        s_wall[3] = -s_wall[3]
        s_neu = rk4_step(s_wall, (1-alpha)*dt, m, q, g, positions)
    
    return s_neu

#Startzustände
states = np.array([
    [1.0, 45.0, 10.0, 0.0]
    [99.0, 55.0, -10.0, 0.0]
    [10.0, 50.0, 15.0, -15.0]
    [20.0, 30.0, -15.0, -15.0]
    [80.0, 70.0, 15.0, 15.0]
    [80.0, 60.0, 15.0, 15.0]
    [80.0, 50.0, 15.0, 15.0] 
], dtype=float)

n_particles = len(states)

trajectories = np.zeros((steps+1, n_particles, 2))
trajectories[0] = states[:, :2]

#Zeit
for t in range(steps):
    new_states = np.zeros_like(states)
    for i in range(N):
        other_positions = np.delete(states[:, :2], i, axis=0)
        new_states[i] = reflect_particle(states[i], dt, m ,q, g, other_positions)
    states = new_states
    trajectories[t+1] = states[:, :2]
    
#Simulierung
plt.figure(figsize=(8,6))
for i in range(n_particles):
    plt.plt(trajectories[:, i, 0], trajectories[:, i, 1], label=f'Particle {i+1}')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Bahnen der Teilchen über 10 Sekunden')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.legend()
plt.show()    
    
    
    
    
    
    
    
    
    
    
    
    