#DGL und Reflexion an den Wänden

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


N = 10
m = 1.0
q = 1.0
g = 0
dt = 0.01
steps = 11
positions = np.random.rand(N, 2) * 100
rng = np.random.default_rng(0)
velocities = rng.uniform(-20, 20, size=(N, 2))
states = np.hstack([positions, velocities])


def f(s, m, q, g, positions):
    x, y, vx, vy = s
    ax, ay = 0.0, g #Gravitation in y-Richtung
    
    for pos in positions:
        dx = x - pos[0]
        dy = y - pos[1]
        r3 = (dx**2 + dy**2)**1.5
        if r3 != 0:
            ax -= q**2 / m * dx / r3
            ay -= q**2 / m * dy / r3
            
    return np.array([vx, vy, ax, ay])

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
        alpha = (wall_x - s[0]) / (s_neu[0] - s[0])
        s_wall = rk4_step(s, alpha*dt, m, q, g, positions)
        s_wall[2] = -s_wall[2]
        s_neu = rk4_step(s_wall, (1-alpha)*dt, m, q, g, positions)
        
    if s_neu[1] < y_min or s_neu[1] > y_max:
        wall_y = y_min if s_neu [1] < y_min else y_max
        alpha = (wall_y - s[1]) / (s_neu[1] - s[1])
        s_wall = rk4_step(s, alpha*dt, m, q, g, positions)
        s_wall[3] = -s_wall[3]
        s_neu = rk4_step(s_wall, (1-alpha)*dt, m, q, g, positions)
    
    return s_neu

for t in range(steps):
    new_states = np.zeros_like(states)
    for i in range(N):
        other_positions = np.delete(states[:, :2], i, axis=0)
        new_states[i] = reflect_particle(states[i], dt, m ,q, g, other_positions)
    states = new_states
    
plt.figure()
plt.scatter(states[:,0], states[:,1])
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.show()


fig, ax = plt.subplots()
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
scat = ax.scatter(states[:,0], states[:,1])

def update(frame):
    global states
    new_states = np.empty_like(states)
    for i in range(N):
        other_pos = np.delete(states[:, :2], i, axis=0)
        new_states[i] = reflect_particle(states[i], dt, m, q, g, other_pos)
    states = new_states
    scat.set_offsets(states[:, :2])
    return scat,
    
ani = FuncAnimation(fig, update, frames=steps, interval=10, blit=True)
plt.show()
    