import numpy as np
import pandas as pd

class OracleCore:
    def __init__(self):
        # THE GLOBAL STATE VECTOR (S)
        # Index 0: Traffic Congestion (0.0 - 1.0)
        # Index 1: Economic Panic (0.0 - 1.0)
        # Index 2: Grid Stability (0.0 = Blackout, 1.0 = Stable)
        self.state_vector = np.array([0.0, 0.0, 1.0]) 
        
        # THE TRANSITION MATRIX (T)
        # This represents the "Laws of Reality" (How one sector affects another)
        # Example: High Traffic (Row 0) causes Economic Panic (Col 1) to rise.
        self.transition_matrix = np.array([
            [0.9,  0.2, -0.1],  # Traffic self-sustains + adds Panic + drains Grid
            [0.0,  0.9,  0.0],  # Panic self-sustains
            [-0.1, -0.2, 0.8]   # Traffic & Panic degrade Grid Stability
        ])

    def sync_senses(self, traffic_data, finance_data, energy_data):
        """
        Fuses raw data from agents into the Normalized State Vector
        """
        # 1. Normalize Traffic (0-100% -> 0.0-1.0)
        t_score = traffic_data.get('congestion', 0)
        
        # 2. Normalize Finance (Panic Score 0-100 -> 0.0-1.0)
        f_score = finance_data.get('panic_score', 0) / 100.0
        
        # 3. Normalize Energy (ON=1.0, OFF=0.0)
        e_score = 1.0 if energy_data.get('status') == "GRID ACTIVE" else 0.0
        
        # Update the Vector
        self.state_vector = np.array([t_score, f_score, e_score])
        return self.state_vector

    def simulate_future(self, steps=3):
        """
        Predicts the future state S(t+n) using Matrix Multiplication
        """
        future_states = []
        current_s = self.state_vector.copy()
        
        for _ in range(steps):
            # THE MASTER EQUATION: S(t+1) = T * S(t)
            next_s = np.dot(self.transition_matrix, current_s)
            
            # Clip values to stay realistic (0.0 to 1.0)
            next_s = np.clip(next_s, 0.0, 1.0)
            
            future_states.append(next_s)
            current_s = next_s
            
        return future_states

    def get_system_health(self):
        """
        Returns the overall 'Health' of the System (Inverse of Entropy)
        """
        # Simple average of stability metrics
        # (1 - Traffic) + (1 - Panic) + (Grid)
        t, f, e = self.state_vector
        health = ((1.0 - t) + (1.0 - f) + e) / 3.0
        return health * 100