import requests
import urllib.parse

class SatelliteUplink:
    def __init__(self):
        self.key = "9ejSySwpBOXEAnPkPpjbv8LuVmBmenrQ"
        self.traffic_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
        self.search_url = "https://api.tomtom.com/search/2/search"

    def find_coordinates(self, location_name):
        """Now returns the STREET NAME too, so you know if you missed."""
        try:
            # Safe encoding
            query = urllib.parse.quote(location_name)
            url = f"{self.search_url}/{query}.json?key={self.key}&limit=1"
            
            response = requests.get(url, timeout=5).json()
            if response['results']:
                result = response['results'][0]
                position = result['position']
                
                # Get the address or street name
                address = result.get('address', {}).get('freeformAddress', 'Unknown Location')
                
                return position['lat'], position['lon'], address
            else:
                return None, None, None
        except:
            return None, None, None

    def get_traffic_data(self, lat, lng):
        try:
            url = f"{self.traffic_url}?key={self.key}&point={lat},{lng}"
            response = requests.get(url, timeout=5).json()
            data = response['flowSegmentData']
            
            current_speed = data['currentSpeed']
            free_flow_speed = data['freeFlowSpeed']
            delay = data['currentTravelTime'] - data['freeFlowTravelTime']
            
            if free_flow_speed > 0:
                congestion = 1 - (current_speed / free_flow_speed)
            else:
                congestion = 0.0
            
            return {
                "congestion": max(0.0, min(1.0, congestion)),
                "delay_seconds": max(0, delay),
                "speed": current_speed
            }
        except:
            return {"congestion": 0.0, "delay_seconds": 0, "speed": 0}