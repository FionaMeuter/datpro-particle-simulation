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
