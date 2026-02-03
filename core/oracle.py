import numpy as np
import pandas as pd

class OracleCore:
    def __init__(self):
        # [Traffic, Panic, Energy, Bio]
        self.state_vector = np.array([0.2, 0.1, 1.0, 0.3]) 
        
        # Transition Matrix (4x4)
        self.transition_matrix = np.array([
            [0.8,  0.0, -0.1,  0.0],
            [0.2,  0.9, -0.3,  0.4],
            [-0.1, -0.1, 0.9,  0.0],
            [0.4,  0.0, -0.5,  0.8]
        ])

    # THIS IS THE CRITICAL FIX: IT NOW ACCEPTS 'b_data'
    def sync_senses(self, t_data, f_data, e_data, b_data):
        t = t_data.get('congestion', 0)
        f = f_data.get('panic_score', 0) / 100.0
        e = 1.0 if e_data.get('status') == "GRID ACTIVE" else 0.0
        b = min(1.0, b_data.get('aqi', 0) / 100.0)
        
        self.state_vector = np.array([t, f, e, b])
        return self.state_vector

    def simulate_future(self, steps=12, impact_override=None):
        future_states = []
        current_s = self.state_vector.copy()
        
        if impact_override:
            current_s = current_s + np.array(impact_override)
            current_s = np.clip(current_s, 0.0, 1.0)

        for _ in range(steps):
            next_s = np.dot(self.transition_matrix, current_s)
            next_s = np.clip(next_s, 0.0, 1.0)
            future_states.append(next_s)
            current_s = next_s
            
        return future_states

    def get_system_health(self):
        t, f, e, b = self.state_vector
        return ((1.0 - t) + (1.0 - f) + e + (1.0 - b)) / 4.0 * 100