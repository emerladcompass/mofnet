"""
MOFNet Extended - 8 Clinical Variables
Compatible with Termux, no dependencies
"""

import random
import json
import time
from .termux_ml import SimpleLinearRegression, SimpleDecisionTree

def calculate_epri(heart_rate, sbp, dbp, rr, spo2, gcs=15, urine_output=50, temperature=37.0):
    """
    Extended Physiological Resilience Index (8 variables)
    
    Parameters:
    -----------
    gcs : int (3-15)
        Glasgow Coma Scale
    urine_output : float (ml/hour)
        Urine output per hour
    temperature : float (°C)
        Body temperature (35-40)
    
    Returns:
    --------
    float : ePRI value (0-1)
    """
    # 1. Calculate base PRI (original 5 variables)
    # Normalize original 5 variables
    hr_n = max(0, 1 - abs(heart_rate - 72) / 100)
    bp_n = max(0, 1 - abs((sbp + dbp * 2) / 3 - 93) / 100)
    rr_n = max(0, 1 - abs(rr - 16) / 30)
    spo2_n = max(0, (spo2 - 80) / 20)
    
    base_pri = (hr_n + bp_n + rr_n + spo2_n) / 4
    
    # 2. Neurological factor (GCS: 3-15)
    neuro_factor = gcs / 15.0  # 1.0 if GCS=15, 0.2 if GCS=3
    
    # 3. Renal factor (Urine output: ml/hour)
    renal_factor = 1.0 if urine_output >= 30 else (urine_output / 30.0)
    
    # 4. Temperature factor (Normal: 37°C)
    temp_factor = 1.0 - (abs(temperature - 37.0) * 0.03)
    temp_factor = max(0.7, min(1.0, temp_factor))
    
    # 5. Final calculation
    epri = base_pri * neuro_factor * renal_factor * temp_factor
    return round(max(0, min(1, epri)), 3)

def classify_epri_level(epri):
    """
    Classify ePRI level (stricter thresholds)
    """
    if epri >= 0.80:
        return "Excellent"
    elif epri >= 0.65:
        return "Good"
    elif epri >= 0.45:
        return "Moderate"
    else:
        return "Poor"

class ExtendedMOFNetPredictor:
    """Extended predictor for 8 clinical variables"""
    
    def __init__(self):
        self.regression_model = SimpleLinearRegression()
        self.classification_model = SimpleDecisionTree(max_depth=4)
        self.trained = False
    
    def generate_training_data(self, n_samples=100):
        """Generate synthetic data with 8 variables"""
        X = []
        y = []
        
        for _ in range(n_samples):
            # Generate 8 clinical variables
            hr = random.randint(40, 180)
            sbp = random.randint(70, 200)
            dbp = random.randint(40, 120)
            rr = random.randint(8, 40)
            spo2 = random.randint(75, 100)
            gcs = random.randint(3, 15)
            urine = random.randint(0, 100)  # ml/hour
            temp = round(random.uniform(35.0, 40.0), 1)
            
            # Calculate extended risk
            risk = 0
            # Original 5 variables
            if hr < 60 or hr > 100: risk += 0.15
            if sbp < 90 or sbp > 140: risk += 0.15
            if spo2 < 92: risk += 0.20
            if rr < 12 or rr > 20: risk += 0.15
            # New 3 variables
            if gcs < 9: risk += 0.20  # Severe neurological impairment
            if urine < 30: risk += 0.10  # Oliguria
            if temp < 36.0 or temp > 38.5: risk += 0.05
            
            # Classification
            if risk < 0.3:
                cls = 0  # Low
            elif risk < 0.6:
                cls = 1  # Medium
            else:
                cls = 2  # High
                
            X.append([hr, sbp, dbp, rr, spo2, gcs, urine, temp])
            y.append(cls)
            
        return X, y
    
    def train(self):
        """Train extended model"""
        X, y = self.generate_training_data(80)
        
        # Train regression on first variable (HR)
        y_reg = [x[0]/180 for x in X]  # Normalized HR as proxy
        self.regression_model.fit([x[0] for x in X], y_reg)
        
        # Train classification
        self.classification_model.fit(X, y)
        
        self.trained = True
        return True
    
    def predict_risk(self, vitals):
        """Predict risk with 8 variables"""
        if not self.trained:
            self.train()
        
        # Prepare features (8 variables)
        features = [
            vitals.get('heart_rate', 72),
            vitals.get('sbp', 120),
            vitals.get('dbp', 80),
            vitals.get('rr', 16),
            vitals.get('spo2', 98),
            vitals.get('gcs', 15),
            vitals.get('urine_output', 50),
            vitals.get('temperature', 37.0)
        ]
        
        # Get classification
        cls = self.classification_model.predict([features])[0]
        
        # Get regression score
        reg_score = self.regression_model.predict(features[0])
        
        # Risk levels
        risk_levels = ['Low', 'Medium', 'High', 'Critical']
        level = risk_levels[min(cls, 3)]
        
        return {
            'risk_level': level,
            'risk_score': float(reg_score),
            'classification': int(cls),
            'organ_scores': self._calculate_organ_scores(vitals),
            'epri': calculate_epri(**vitals) if all(k in vitals for k in ['heart_rate', 'sbp', 'dbp', 'rr', 'spo2', 'gcs', 'urine_output', 'temperature']) else None
        }
    
    def _calculate_organ_scores(self, vitals):
        """Calculate organ-specific risks with extended variables"""
        scores = {}
        
        # Cardiac (HR, BP)
        hr = vitals.get('heart_rate', 72)
        sbp = vitals.get('sbp', 120)
        cardiac = 0
        if hr < 60 or hr > 100: cardiac += 0.6
        if sbp < 90 or sbp > 140: cardiac += 0.4
        scores['cardiac'] = min(cardiac, 1.0)
        
        # Neurological (GCS)
        gcs = vitals.get('gcs', 15)
        scores['neurological'] = 1.0 - (gcs / 15.0)
        
        # Renal (Urine output)
        urine = vitals.get('urine_output', 50)
        scores['renal'] = 0.0 if urine >= 30 else (1.0 - urine/30.0)
        
        # Respiratory (RR, SpO2)
        rr = vitals.get('rr', 16)
        spo2 = vitals.get('spo2', 98)
        resp = 0
        if rr < 12 or rr > 20: resp += 0.5
        if spo2 < 95: resp += 0.5
        scores['respiratory'] = min(resp, 1.0)
        
        # Hepatic (simulated with temperature)
        temp = vitals.get('temperature', 37.0)
        scores['hepatic'] = abs(temp - 37.0) * 0.1
        
        return scores

# Quick test function
def test_extended():
    """Test the extended module"""
    print("🧪 Testing MOFNet Extended (8 variables)...")
    
    # Test ePRI calculation
    vitals = {
        'heart_rate': 80,
        'sbp': 120,
        'dbp': 80,
        'rr': 16,
        'spo2': 98,
        'gcs': 15,
        'urine_output': 50,
        'temperature': 37.0
    }
    
    epri = calculate_epri(**vitals)
    print(f"✅ ePRI: {epri} - {classify_epri_level(epri)}")
    
    # Test predictor
    predictor = ExtendedMOFNetPredictor()
    predictor.train()
    
    result = predictor.predict_risk(vitals)
    print(f"✅ Risk Level: {result['risk_level']}")
    print(f"✅ Organ Scores: {result['organ_scores']}")
    
    return True

if __name__ == "__main__":
    test_extended()
