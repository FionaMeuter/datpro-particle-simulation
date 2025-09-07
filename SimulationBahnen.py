#Simulierung Bahnen von Teilchen

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 

#Konstanten
N = 7 # Anzahl der Teilchen
m = 1.0 # Masse eines Teilchens
q = 50 #Ladung des Teilchens
g = -10.0 # Gravitationskraft 
dt = 0.001 # Zeitschritte
steps = 10000
y_min, y_max = 0, 100 # Höhe der Box
x_min, x_max = 0, 100 # Breite der Box


#Klasse der Teilchen
class Particle:
    def __init__(self, position, velocity, mass): #Initiallisierung von Teilchen mit Position, Geschwindigkeit und Masse
        self.position = np.array(position, dtype=float) #Position
        self.velocity = np.array(velocity, dtype=float) #Geschwindigkeit
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



#Startzustände zur Simulation
states = np.array([
    [1.0, 45.0, 10.0, 0.0],
    [99.0, 55.0, -10.0, 0.0],
    [10.0, 50.0, 15.0, -15.0],
    [20.0, 30.0, -15.0, -15.0],
    [80.0, 70.0, 15.0, 15.0],
    [80.0, 60.0, 15.0, 15.0],
    [80.0, 50.0, 15.0, 15.0] 
], dtype=float)

N = len(states)

tracks = np.zeros((steps+1, N, 2)) #Anzahl Zeitschirtte und Startzustand
tracks[0] = states[:, :2] #erster Zeitschritt mit x und y

#Zeitschritte
for t in range(steps):
    new_states = np.zeros_like(states) #Neue Positionen des Zeitschrittes speichern 
    for i in range(N): #Schleife für Teilchen und dessen Position
        other_positions = np.delete(states[:, :2], i, axis=0) #aktuelle Position Teilchen word gelöscht
        s_neu = rk4_step(states[i], dt, m, q, g, other_positions)
        s_neu = reflect_particle(s_neu, dt, m, q, g, other_positions)
        new_states[i] = s_neu #speichert neues Ergebnis Teilchen
    states = new_states #Aktualisierung Gesamtzustand
    tracks[t+1] = states[:, :2] #Neue Position Teilchen in Bahnen


#Simulierung und Animation

points, = plt.plot([], [], 'o', markersize=4) #Definierung der Teilchen als Punkte

def update(frame): #Bilder werden aufgerufen
    x = tracks[frame, :, 0]#Koordinaten von Teilchen für dieses Zeitschritt
    y = tracks[frame, :, 1]
    points.set_data(x, y)
    return points, #Aktualisierung der Teilchen

ani = FuncAnimation( # erstellt die Animation über alle Zeitschritte
    plt.gcf(), update, frames=len(tracks),
    interval=20, blit=True #einmal Wartezeit für die einezlnen Bilder in Millisekunden
    )


for i in range(N):
    plt.plot(tracks[:, i, 0], tracks[:, i, 1], label=f'Particle {i+1}')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Bahnen der Teilchen über 10 Sekunden')
plt.gca().set_aspect('equal')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.legend()
plt.show() 
