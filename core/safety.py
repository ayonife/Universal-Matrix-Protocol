class SafetyProtocol:
    def validate_data(self, data, loss):
        # 1. Check for Sensor Errors
        if data['delay_seconds'] > 18000:
            return {"safe": False, "msg": "⚠️ ANOMALY: Sensor Error (Delay > 5hrs)"}
        
        # 2. Check for Hallucinations
        if loss > 50_000_000_000:
            return {"safe": False, "msg": "⚠️ ALERT: Value Exceeds Logic Limit"}
            
        return {"safe": True, "msg": "✅ Verified"}