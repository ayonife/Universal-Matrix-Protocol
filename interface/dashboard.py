import os
import time

# Cyberpunk Color Palette
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Track when the system started
START_TIME = time.monotonic()

def _format_uptime():
    elapsed = int(time.monotonic() - START_TIME)
    hours, rem = divmod(elapsed, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def render_matrix(loc, cong, delay, loss, safe):
    # Clear screen command that works on both Windows and Phone
    os.system('cls' if os.name == 'nt' else 'clear')
    
    uptime = _format_uptime()
    delay_minutes = int(delay / 60)
    congestion_pct = int(cong * 100)
    
    # Dynamic Bar Graph
    bar_length = 24
    filled = int(cong * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)

    # THE CYBERPUNK INTERFACE
    print(f"{MAGENTA}{BOLD}╔══════════════════════════════════════════════╗{RESET}")
    print(f"{MAGENTA}{BOLD}║   UNIVERSAL MATRIX PROTOCOL • PHASE 0 (LN)   ║{RESET}")
    print(f"{MAGENTA}{BOLD}╚══════════════════════════════════════════════╝{RESET}")
    
    print(f"{CYAN}📍 SECTOR:{RESET} {BOLD}{loc}{RESET}")
    print(f"{CYAN}⏱️  DELAY:{RESET} {YELLOW}{delay_minutes}m{RESET}")
    print(f"{CYAN}⏳ SYSTEM UPTIME:{RESET} {GREEN}{uptime}{RESET}")

    print(f"\n{CYAN}🚦 TRAFFIC LOAD{RESET}")
    print(f"{GREEN}[{bar}]{RESET} {BOLD}{congestion_pct}%{RESET}")
    print(f"{MAGENTA}{'─' * 46}{RESET}")

    if safe["safe"]:
        print(f"{CYAN}💸 ECONOMIC BURN:{RESET} {RED}₦ {loss:,.2f}{RESET} / HR")
        print(f"{GREEN}✔ SAFETY PROTOCOL:{RESET} {safe['msg']}")
    else:
        print(f"{RED}⚠️ {safe['msg']}{RESET}")

    print(f"\n{CYAN}[SYSTEM STATUS]{RESET} {GREEN}LIVE{RESET} • UPDATE: 10s")