import pandas as pd
import matplotlib.pyplot as plt

class WarRoom:
    def __init__(self, filename="matrix_logs.csv"):
        self.filename = filename

    def generate_graph(self):
        try:
            # 1. Read the Black Box Data
            df = pd.read_csv(self.filename)

            # 2. Clean the Data (Remove '₦' and commas to do math)
            df['BURN_RATE (NGN)'] = df['BURN_RATE (NGN)'].astype(str).str.replace('₦', '').str.replace(',', '').astype(float)
            
            # 3. Filter: Only show locations with Burn Rate > 0
            active_sectors = df[df['BURN_RATE (NGN)'] > 0]
            
            if active_sectors.empty:
                print("No economic burn detected yet. Scan more locations!")
                return

            # 4. Create the Chart
            plt.figure(figsize=(10, 6))
            
            # Bar Chart: Location vs Money
            bars = plt.barh(active_sectors['LOCATION'], active_sectors['BURN_RATE (NGN)'], color='#ff4444')
            
            # Styling (Cyberpunk Theme)
            plt.style.use('dark_background')
            plt.title('⚠️ REAL-TIME ECONOMIC BURN RATE (LAGOS)', fontsize=14, color='cyan')
            plt.xlabel('LOSS IN NAIRA (millions)', color='white')
            plt.grid(axis='x', linestyle='--', alpha=0.3)
            
            # Add text labels on the bars
            for bar in bars:
                width = bar.get_width()
                label_y = bar.get_y() + bar.get_height() / 2
                plt.text(width, label_y, f' ₦{width:,.0f}', va='center', color='yellow')

            print("📊 GENERATING WAR ROOM DISPLAY...")
            plt.tight_layout()
            
            # Save the image instead of showing it
            plt.savefig('war_room_report.png')
            print(f"✔ REPORT SAVED: 'war_room_report.png' (Check your file explorer)")

        except Exception as e:
            print(f"Error generating graph: {e}")

# Self-test block
if __name__ == "__main__":
    viz = WarRoom()
    viz.generate_graph()