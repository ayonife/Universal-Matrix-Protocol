import time
from infrastructure.tomtom_client import SatelliteUplink
from core.economics import EconomicMatrix
from core.safety import SafetyProtocol
from core.writer import PropagandaEngine
from core.memory import BlackBox
from core.midas import FinancialOracle
from core.hermes import Messenger      # <--- NEW AGENT CONNECTED
import interface.dashboard as ui

# System Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# 🎯 THE SENTINEL WATCH LIST
SECTORS = [
    {"type": "traffic", "id": "Lekki-Epe Expressway"},
    {"type": "traffic", "id": "Ozumba Mbadiwe Avenue"},
    {"type": "finance", "id": "BTC-USD"}, # Bitcoin
    {"type": "finance", "id": "GC=F"}     # Gold
]

# Initialize The Swarm
grok = SatelliteUplink()
deepseek = EconomicMatrix()
kimi = SafetyProtocol()
claude = PropagandaEngine()
recorder = BlackBox()
midas = FinancialOracle()
hermes = Messenger()          # <--- HERMES IS ONLINE

def scan_traffic(target_name):
    print(f"{CYAN}📡 SCANNING SECTOR: '{target_name.upper()}'...{RESET}")
    search_term = target_name if "lagos" in target_name.lower() else target_name + " Lagos"
    lat, lng, address = grok.find_coordinates(search_term) 
    
    if lat:
        data = grok.get_traffic_data(lat, lng)
        loss = deepseek.compute_loss_vector(data['congestion'], data['delay_seconds']/60)
        security = kimi.validate_data(data, loss)
        
        ui.render_matrix(address, data['congestion'], data['delay_seconds'], loss, security)
        recorder.log_event(address, data['congestion'], data['delay_seconds'], loss, security['msg'])
        
        # 🚨 TRIGGER: HIGH TRAFFIC ALERT
        if data['congestion'] > 0.80: # If traffic is over 80%
            msg = (f"🚨 *GRIDLOCK ALERT*\n"
                   f"📍 {target_name}\n"
                   f"🚦 Load: {int(data['congestion']*100)}%\n"
                   f"💸 Burn: ₦{loss:,.0f}/hr")
            hermes.send_alert(msg)
            print(f"{RED}⚡ ALERT SENT TO TELEGRAM{RESET}")
            
        return True
    return False

def scan_finance(ticker):
    print(f"{YELLOW}💰 ANALYZING MARKET: {ticker}...{RESET}")
    market_data = midas.get_asset_health(ticker)
    
    if market_data:
        print(f"   Price: ${market_data['price']:,.2f}")
        print(f"   Panic: {market_data['panic_score']:.1f}%")
        
        # 🚨 TRIGGER: MARKET CRASH ALERT
        if market_data['panic_score'] > 80:
            msg = (f"🚨 *MARKET CRASH WARNING*\n"
                   f"📉 Asset: {ticker}\n"
                   f"💥 Panic Score: {market_data['panic_score']:.0f}%\n"
                   f"💰 Price: ${market_data['price']:,.2f}")
            hermes.send_alert(msg)
            print(f"{RED}⚡ ALERT SENT TO TELEGRAM{RESET}")
            
        return True
    return False

def manual_mode():
    while True:
        target = input(f"\n{GREEN}root@omnix:~$ ENTER TARGET > {RESET}")
        if target.lower() == 'menu': break
        
        if "=" in target or "-" in target:
            scan_finance(target.upper())
        else:
            scan_traffic(target)

def main_menu():
    while True:
        ui.os.system('cls' if ui.os.name == 'nt' else 'clear')
        print(f"\n{CYAN}:: UNIVERSAL MATRIX PROTOCOL (CONNECTED) ::{RESET}")
        print(f"{GREEN}[1] ACTIVATE SENTINEL (Auto-Alerts){RESET}")
        print(f"{GREEN}[2] MANUAL SCAN{RESET}")
        
        choice = input(f"\n{CYAN}SELECT > {RESET}")
        
        if choice == "1":
            try:
                while True:
                    for target in SECTORS:
                        if target['type'] == 'traffic': scan_traffic(target['id'])
                        elif target['type'] == 'finance': scan_finance(target['id'])
                        print(f"\n{GREEN}>> NEXT SCAN IN 5s...{RESET}")
                        time.sleep(5)
            except KeyboardInterrupt: break
        elif choice == "2":
            manual_mode()

if __name__ == "__main__":
    main_menu()