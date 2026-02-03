import random

class EnergyGrid:
    def __init__(self):
        self.diesel_price = 1350  # Current price per Liter
        self.petrol_price = 1150  # Current price for small gens (I-better-pass-my-neighbor)
        
        # LAGOS POWER SPECS
        # Est. 5 Million households. 
        # When NEPA takes light, ~60% turn on generators.
        self.active_generators = {
            "industrial": 5000,    # Big Mikano/CAT gens (Banks, Malls)
            "household": 2500000,  # Small petrol gens ("I pass my neighbor")
            "mid_size": 200000     # Silent diesel gens (Estates)
        }

    def check_grid_status(self):
        """
        Simulates the Grid Status based on time of day.
        (In a real version, we would scrape Twitter for 'No Light' tweets).
        """
        # Random simulation for now: 40% chance of light, 60% chance of darkness
        status = "ON" if random.random() > 0.6 else "OFF"
        return status

    def calculate_burn_rate(self, grid_status):
        if grid_status == "ON":
            return {"status": "GRID ACTIVE", "burn_rate": 0, "generators_on": 0}
        
        # IF GRID IS OFF: CALCULATE THE BURN
        # 1. Industrial (Burns ~30 Liters/hr Diesel)
        ind_cost = self.active_generators["industrial"] * 30 * self.diesel_price
        
        # 2. Mid-Size (Burns ~5 Liters/hr Diesel)
        mid_cost = self.active_generators["mid_size"] * 5 * self.diesel_price
        
        # 3. Household (Burns ~0.7 Liters/hr Petrol)
        home_cost = self.active_generators["household"] * 0.7 * self.petrol_price
        
        total_burn = ind_cost + mid_cost + home_cost
        total_gens = sum(self.active_generators.values())
        
        return {
            "status": "🔴 BLACKOUT",
            "burn_rate": total_burn,
            "generators_on": total_gens
        }