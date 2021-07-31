HEIGHT_THRESHOLD = 1 # meter

class ShotCounter:
    def __init__(self):
        self.attempts = 0
        self.in_air = False
    
    def update(self, drone_height, ball):
        if drone_height > HEIGHT_THRESHOLD and ball.centroid[1] < 360:
            if not self.in_air:
                self.in_air = True
                self.attempts += 1
                print(f"Shot attempts: {self.attempts}")
        else:
            if self.in_air:
                self.in_air = False
