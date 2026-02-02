import time
from infrastructure.tomtom_client import SatelliteUplink
from core.economics import EconomicMatrix
from core.safety import SafetyProtocol
import interface.dashboard as ui

# Target: Ikorodu Road Coordinates
IKORODU_COORDS = (6.6194, 3.5105)

def activate_matrix():
    # Initialize the Swarm
    grok = SatelliteUplink()
    deepseek = EconomicMatrix()
    kimi = SafetyProtocol()
    
    while True:
        try:
            # 1. Grok fetches Data
            data = grok.get_traffic_data(*IKORODU_COORDS)
            
            # 2. DeepSeek calculates Loss
            loss = deepseek.compute_loss_vector(data['congestion'], data['delay_seconds']/60)
            
            # 3. Kimi checks Safety
            security = kimi.validate_data(data, loss)
            
            # 4. ChatGPT shows Dashboard
            ui.render_matrix("Ikorodu Road", data['congestion'], data['delay_seconds'], loss, security)
            
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\nShutting down...")
            break

if __name__ == "__main__":
    activate_matrix()