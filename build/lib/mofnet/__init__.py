"""
MOFNET - Medical MOF Prediction
Version 1.0.2 - Fixed calculate_pri_from_dict
"""

__version__ = "1.0.2"
__author__ = "Samir Baladi"
__email__ = "emerladcompass@gmail.com"

def calculate_pri(hr, bp_sys, bp_dia, rr, spo2, **kwargs):
    """
    Calculate Patient Resilience Index.
    Returns value between 0.0 and 1.0.
    """
    # Simple but proper calculation
    hr_score = max(0.0, 1.0 - abs(hr - 80) / 80)
    map_val = bp_dia + (bp_sys - bp_dia) / 3
    map_score = max(0.0, 1.0 - abs(map_val - 85) / 85)
    rr_score = max(0.0, 1.0 - abs(rr - 16) / 24)
    spo2_score = max(0.0, min(1.0, (spo2 - 70) / 30))
    
    # Weighted average
    pri = 0.3 * hr_score + 0.3 * map_score + 0.2 * rr_score + 0.2 * spo2_score
    
    return round(max(0.0, min(pri, 1.0)), 3)

def calculate_pri_from_dict(vitals):
    """
    Calculate PRI from dictionary.
    Supports multiple key naming conventions.
    """
    # Extract values with defaults
    hr = vitals.get('hr') or vitals.get('heart_rate') or vitals.get('Heart_Rate') or 80
    bp_sys = vitals.get('bp_sys') or vitals.get('blood_pressure_systolic') or vitals.get('Systolic_BP') or 120
    bp_dia = vitals.get('bp_dia') or vitals.get('blood_pressure_diastolic') or vitals.get('Diastolic_BP') or 80
    rr = vitals.get('rr') or vitals.get('respiratory_rate') or vitals.get('RespiratoryRate') or 16
    spo2 = vitals.get('spo2') or vitals.get('oxygen_saturation') or vitals.get('O2_Saturation') or 98
    
    return calculate_pri(
        hr=hr,
        bp_sys=bp_sys,
        bp_dia=bp_dia,
        rr=rr,
        spo2=spo2
    )

def classify_pri_level(pri_score):
    """
    Classify PRI score into clinical categories.
    """
    if pri_score < 0.3:
        return "Critical"
    elif pri_score < 0.5:
        return "Poor"
    elif pri_score < 0.7:
        return "Moderate"
    elif pri_score < 0.85:
        return "Good"
    else:
        return "Excellent"

__all__ = [
    "calculate_pri",
    "calculate_pri_from_dict",
    "classify_pri_level"
]

# Print helpful message on import
print(f"✅ MOFNET v{__version__} loaded successfully")
