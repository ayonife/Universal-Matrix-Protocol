import time
from infrastructure.tomtom_client import SatelliteUplink
from core.economics import EconomicMatrix
from core.safety import SafetyProtocol
from core.writer import PropagandaEngine
from core.memory import BlackBox
from core.midas import FinancialOracle
import interface.dashboard as ui  # <--- THIS WAS MISSING. I ADDED IT BACK.

# System Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# 🎯 THE HYBRID TARGET LIST
SECTORS = [
    {"type": "traffic", "id": "Lekki-Epe Expressway"},
    {"type": "traffic", "id": "Ikorodu Road"},
    {"type": "traffic", "id": "Ozumba Mbadiwe Avenue"},
    {"type": "finance", "id": "GC=F"},    # Gold Futures
    {"type": "finance", "id": "BTC-USD"}, # Bitcoin
    {"type": "finance", "id": "NGN=X"}    # Naira vs Dollar
]

def activate_sentinel():
    # Initialize The Swarm
    grok = SatelliteUplink()
    deepseek = EconomicMatrix()
    kimi = SafetyProtocol()
    claude = PropagandaEngine()
    recorder = BlackBox()
    midas = FinancialOracle()
    
    print(f"{CYAN}:: UNIVERSAL MATRIX PROTOCOL (HYBRID SENTINEL) ::{RESET}")
    print(f"{GREEN}✔ TRAFFIC & FINANCIAL SENSORS ACTIVE.{RESET}\n")
    
    while True:
        try:
            for target in SECTORS:
                
                # ==========================================
                # MODE A: TRAFFIC SCANS
                # ==========================================
                if target['type'] == 'traffic':
                    print(f"{CYAN}📡 SCANNING SECTOR: '{target['id'].upper()}'...{RESET}")
                    
                    # 1. Search
                    search_term = target['id'] if "lagos" in target['id'].lower() else target['id'] + " Lagos"
                    lat, lng, address = grok.find_coordinates(search_term) 
                    
                    if lat:
                        # 2. Analyze
                        data = grok.get_traffic_data(lat, lng)
                        loss = deepseek.compute_loss_vector(data['congestion'], data['delay_seconds']/60)
                        security = kimi.validate_data(data, loss)
                        
                        # 3. Visualize
                        ui.render_matrix(address, data['congestion'], data['delay_seconds'], loss, security)
                        
                        # 4. Save to CSV
                        print(f"\n{CYAN}💾 LOGGING TRAFFIC EVENT...{RESET}")
                        recorder.log_event(address, data['congestion'], data['delay_seconds'], loss, security['msg'])
                        
                        # 5. Propaganda
                        tweet, _, _ = claude.generate_report(address, loss, data['delay_seconds'])
                        print(f"{CYAN}🐦 CONTENT GENERATED{RESET}")

                    else:
                        print(f"❌ {RED}SECTOR NOT FOUND: {target['id']}{RESET}")

                # ==========================================
                # MODE B: FINANCIAL SCANS
                # ==========================================
                elif target['type'] == 'finance':
                    print(f"{YELLOW}💰 ANALYZING MARKET: {target['id']}...{RESET}")
                    
                    market_data = midas.get_asset_health(target['id'])
                    
                    if market_data:
                        # Display Financial Dashboard
                        print(f"   {GREEN}Price:{RESET}       ${market_data['price']:,.2f}")
                        print(f"   {GREEN}Volatility:{RESET}  {market_data['volatility']:.4f}%")
                        print(f"   {GREEN}Panic Score:{RESET} {market_data['panic_score']:.1f}%")
                        
                        # Color code the status
                        status_color = RED if "CRASH" in market_data['status'] else GREEN
                        print(f"   {GREEN}Status:{RESET}      {status_color}{market_data['status']}{RESET}")
                
                # PAUSE between targets
                print(f"\n{GREEN}>> NEXT SCAN IN 5s...{RESET}")
                time.sleep(5)
            
            print(f"\n{CYAN}💤 CYCLE COMPLETE. SLEEPING...{RESET}")
            time.sleep(60)

        except KeyboardInterrupt:
            print(f"\n{RED}🛑 SENTINEL MODE DEACTIVATED.{RESET}")
            break

if __name__ == "__main__":
    activate_sentinel()