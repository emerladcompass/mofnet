"""
Simple predictor for Termux
"""

class SimpleRiskCalculator:
    
    @staticmethod
    def calculate_risk(vitals):
        """Calculate risk from vitals"""
        risk_score = 0
        
        # Heart rate risk
        hr = vitals.get('heart_rate', 72)
        if hr < 60 or hr > 100:
            risk_score += 0.3
        elif hr < 50 or hr > 120:
            risk_score += 0.5
        
        # Blood pressure risk
        sbp = vitals.get('sbp', 120)
        if sbp < 90 or sbp > 140:
            risk_score += 0.3
        elif sbp < 70 or sbp > 180:
            risk_score += 0.5
        
        # Oxygen risk
        spo2 = vitals.get('spo2', 98)
        if spo2 < 95:
            risk_score += 0.2
        elif spo2 < 90:
            risk_score += 0.4
        
        return min(risk_score, 1.0)
    
    @staticmethod
    def classify_risk(score):
        """Classify risk score"""
        if score < 0.3:
            return "Low"
        elif score < 0.6:
            return "Medium"
        else:
            return "High"

# Test
if __name__ == "__main__":
    calc = SimpleRiskCalculator()
    test_vitals = {'heart_rate': 110, 'sbp': 150, 'spo2': 92}
    score = calc.calculate_risk(test_vitals)
    print(f"Risk Score: {score:.2f}")
    print(f"Risk Level: {calc.classify_risk(score)}")
