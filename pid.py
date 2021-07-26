class PIDController:
    def __init__(self, kp: float, ki: float, kd: float, dt: float):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt

        self.prev_err = None
        self.integral = 0.0
    
    def next(self, err: float) -> float:
        self.integral += err * self.dt

        p = self.kp * err
        i = self.ki * self.integral
        d = self.kd * (err - self.prev_err) / self.dt if self.prev_err else 0

        self.prev_err = err
        return p + i + d