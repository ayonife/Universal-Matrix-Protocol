import os
import time

GREEN, RED, CYAN, RESET = "\033[92m", "\033[91m", "\033[96m", "\033[0m"

def render_matrix(loc, cong, delay, loss, safe):
    # Clear screen command that works on both Windows and Phone
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"\n{CYAN}:: UNIVERSAL MATRIX PROTOCOL :: PHASE 0 ::{RESET}")
    print(f"📍 SECTOR: {loc} | ⏱️ DELAY: {int(delay/60)}m")
    
    # Draw the Loading Bar
    bar = "█" * int(cong * 20)
    print(f"🚦 TRAFFIC LOAD: {GREEN}[{bar:<20}]{RESET} {int(cong*100)}%")
    
    print("-" * 40)
    
    # Show the Money or the Warning
    if safe['safe']:
        print(f"💸 ECONOMIC BURN: {RED}₦ {loss:,.2f}{RESET} / HR")
    else:
        print(f"{RED}{safe['msg']}{RESET}")
    
    print(f"\n{CYAN}[SYSTEM STATUS]: LIVE • UPDATING EVERY 10s...{RESET}")