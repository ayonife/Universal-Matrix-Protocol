import time
from infrastructure.tomtom_client import SatelliteUplink
from core.economics import EconomicMatrix
from core.safety import SafetyProtocol
import interface.dashboard as ui

# Colors for input prompt
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def activate_matrix():
    grok = SatelliteUplink()
    deepseek = EconomicMatrix()
    kimi = SafetyProtocol()
    
    # 1. THE INTERACTIVE LOOP
    while True:
        ui.os.system('cls' if ui.os.name == 'nt' else 'clear')
        print(f"\n{CYAN}:: UNIVERSAL MATRIX PROTOCOL ::{RESET}")
        print("Type a location (e.g., 'Ikeja Underbridge', 'Lekki Toll Gate')")
        print("or type 'exit' to quit.\n")
        
        target = input(f"{GREEN}root@omnix:~$ ENTER LOCATION > {RESET}")
        
        if target.lower() in ['exit', 'quit']:
            break
            
        print(f"\n{CYAN}📡 SEARCHING SATELLITES FOR '{target.upper()}'...{RESET}")
        
        # 2. Find the Coordinates AND Address
        # We auto-add "Lagos" to help the search, unless you typed it already
        search_term = target if "lagos" in target.lower() else target + " Lagos"
        
        lat, lng, address = grok.find_coordinates(search_term) 
        
        if lat:
            print(f"{GREEN}✔ TARGET LOCKED:{RESET} {address}")
            print(f"{CYAN}   Coordinates: {lat}, {lng}{RESET}")
            time.sleep(1)
            
            # 3. Get the Reality Data
            data = grok.get_traffic_data(lat, lng)
            loss = deepseek.compute_loss_vector(data['congestion'], data['delay_seconds']/60)
            security = kimi.validate_data(data, loss)
            
            # 4. Show the Dashboard
            # We pass the REAL address found, not just what you typed
            ui.render_matrix(address, data['congestion'], data['delay_seconds'], loss, security)
            
            input(f"\n{CYAN}[PRESS ENTER TO SCAN NEW LOCATION]{RESET}")
            
        else:
            print(f"\n❌ {RED}ERROR: Location not found.{RESET}")
            print(f"   Try a major landmark like 'Ikeja City Mall' or 'Dopemu Bridge'")
            time.sleep(3)

if __name__ == "__main__":
    activate_matrix()
    