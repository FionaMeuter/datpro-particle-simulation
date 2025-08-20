#Teilchen definiert in Klasse

class Particle:
    def __init__(self, position, velocity, mass): #Initiallisierung von Teilchen mit Position, Geschwindigkeit und Masse
        self.position = position #Position
        self.velocity = velocity #Geschwindigkeit
        self.mass = mass #Masse
    
    def move(self, timestep): #Position des Teilchen beruhend auf Geschwindigkeit und Zeit
        self.position = [
            self.position[i] + self.velocity [i]* timestep
            for i in range(len(self.position))
        ]
    def check_boundary(self, box_size):
        for i in range(len(self.position)):
            if self.position[i] < 0 or self.position[i] > box_size[i]:
                self.velocity[i] *= -1


#Beispielwerte Teilchen in 2D Box              
box_size = [10, 10] #Größe der Box
particle = Particle(position=[5, 5], velocity=[1, -1], mass=1.0)

# Simulation für 10 Zeitschritte um zu gucken wie das Teilchen sich mit den Grenzen verhält
timestep = 1
for step in range(10):
    particle.move(timestep)
    particle.check_boundary(box_size)
    print(f"Schritt {step + 1}: Position = {particle.position}, Geschwindigkeit = {particle.velocity}")