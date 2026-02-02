class EconomicMatrix:
    def __init__(self):
        self.hourly_wage = 1500  # NGN
        self.commuters = 9_000_000

    def compute_loss_vector(self, congestion, delay_minutes):
        if delay_minutes <= 0: return 0.0
        
        # 45% of workforce is on the road
        affected = self.commuters * 0.45 * congestion
        
        # The Money Formula
        loss = (delay_minutes / 60) * affected * self.hourly_wage
        
        # Add 15% for fuel & stress (Ripple Effect)
        return round(loss * 1.15, 2)