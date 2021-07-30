from detection import Ball

class BallEstimator:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.radius = 0
        self.dx = 0
    
    def update(self, ball, dt):
        self.dx = (ball.centroid[0] - self.x) / dt
        self.x = ball.centroid[0]
        self.y = ball.centroid[1]
        self.radius = ball.radius

    def estimate(self, dt):
        # Only estimates x direction for now
        self.x = self.x + self.dx * dt
        return Ball((self.x, self.y), self.radius, "")