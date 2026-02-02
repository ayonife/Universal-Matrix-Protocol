import yfinance as yf
import numpy as np

class FinancialOracle:
    def __init__(self):
        pass

    def get_asset_health(self, symbol="GC=F"): # GC=F is Gold Futures
        try:
            # 1. Get Real-Time Data (1 Day, Minute-by-Minute)
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="15m")
            
            if data.empty:
                return None

            # 2. Calculate Volatility (The "Traffic" of Money)
            # Standard Deviation of returns measures fear/uncertainty
            returns = data['Close'].pct_change().dropna()
            volatility = returns.std() * 100 # Percentage
            current_price = data['Close'].iloc[-1]
            
            # 3. The "Crash Probability" (Simplified Eigen-Logic)
            # If volatility spikes > 0.2% in 15 mins, the market is panicking
            panic_level = min(100, (volatility / 0.2) * 100)
            
            status = "STABLE"
            if panic_level > 50: status = "UNSTABLE"
            if panic_level > 80: status = "CRASH WARNING 🚨"

            return {
                "symbol": symbol,
                "price": current_price,
                "volatility": volatility,
                "panic_score": panic_level,
                "status": status
            }

        except Exception as e:
            return None