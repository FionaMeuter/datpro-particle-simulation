#DGL und Reflexion an den Wänden

import numpy as np

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


#Refelxion an Boxgrenzen
x_min, x_max = 0, 100
y_min, y_max = 0, 100

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


    
