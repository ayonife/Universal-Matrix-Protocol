class EconomicMatrix:
    def __init__(self):
        # 1. DATABASE OF ROAD SIZES (The "Physics")
        # format: "Name": {"lanes": number, "length_km": number, "zone_value": NGN/hr}
        self.road_specs = {
            "Lekki-Epe Expressway": {"lanes": 3, "length_km": 15, "zone_value": 8500},
            "Ozumba Mbadiwe Avenue": {"lanes": 3, "length_km": 4, "zone_value": 25000},
            "Third Mainland Bridge": {"lanes": 4, "length_km": 11, "zone_value": 4500},
            "Ikorodu Road": {"lanes": 3, "length_km": 18, "zone_value": 2500},
            "Default": {"lanes": 2, "length_km": 5, "zone_value": 3000}
        }

    def get_car_count(self, road_name, congestion_percentage):
        """
        Calculates exactly how many cars are stuck based on road size.
        Assumption: In traffic, 1 car takes up ~7 meters (including gap).
        Max capacity per lane/km = 1000m / 7m ≈ 140 cars.
        """
        # Find the road spec (or use default if not found)
        spec = self.road_specs.get(road_name, self.road_specs["Default"])
        if road_name not in self.road_specs:
            # Try partial match (e.g. "Lekki" matches "Lekki-Epe")
            for key in self.road_specs:
                if key in road_name:
                    spec = self.road_specs[key]
                    break
        
        # Max cars the road can hold if 100% full
        max_cars = spec["lanes"] * spec["length_km"] * 140 
        
        # Actual cars right now
        actual_cars = max_cars * congestion_percentage
        return int(actual_cars), spec["zone_value"]

    def compute_precise_loss(self, road_name, congestion, fuel_price):
        """
        The Master Formula for Precise Burn Rate
        """
        # 1. Get Physical Car Count
        total_cars, hourly_wage = self.get_car_count(road_name, congestion)
        
        # 2. Calculate Fuel Burn (Physics)
        # Average car with AC on burns 1.2 Liters/hour idling
        fuel_consumption_rate = 1.2 
        fuel_loss = total_cars * fuel_consumption_rate * fuel_price
        
        # 3. Calculate Productivity Loss (Economics)
        # Money lost because people are sitting instead of working
        productivity_loss = total_cars * hourly_wage
        
        # 4. Total Burn
        total_burn = fuel_loss + productivity_loss
        
        return {
            "total_burn": total_burn,
            "fuel_loss": fuel_loss,
            "productivity_loss": productivity_loss,
            "cars_stuck": total_cars
        }