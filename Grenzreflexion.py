import numpy as np

def move_particles(states, dt):
    new_states = []
    for s in states:
        x, y, vx, vy = s
        vx += np.random.uniform (-1, 1)
        vy += np.random.uniform (-1, 1)
        x = (x + vx * dt) % 100
        y = (y + vy * dt) % 100
        new_states.append ([x, y, vx, vy])
    return np.array(new_states)