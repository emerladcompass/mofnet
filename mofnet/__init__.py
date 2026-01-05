"""
MOFNet - Multi-Organ Failure Network
Medical system for early prediction of multi-organ failure
"""

__version__ = "1.0.2"
__author__ = "Samir Baladi"
__email__ = "emerladcompass@gmail.com"

def calculate_pri(heart_rate, sbp, dbp, rr, spo2):
    """
    Calculate Physiological Resilience Index (PRI)
    
    Parameters:
    -----------
    heart_rate : int
        Heart rate in beats per minute
    sbp : int
        Systolic blood pressure in mmHg
    dbp : int
        Diastolic blood pressure in mmHg
    rr : int
        Respiratory rate in breaths per minute
    spo2 : int
        Oxygen saturation percentage
    
    Returns:
    --------
    float : PRI value between 0 and 1
    """
    # Normalize values
    hr_n = max(0, 1 - abs(heart_rate - 72) / 100)
    bp_n = max(0, 1 - abs((sbp + dbp * 2) / 3 - 93) / 100)
    rr_n = max(0, 1 - abs(rr - 16) / 30)
    spo2_n = max(0, (spo2 - 80) / 20)
    
    # Calculate average
    pri = (hr_n + bp_n + rr_n + spo2_n) / 4
    return round(pri, 3)

def classify_pri_level(pri):
    """
    Classify PRI level
    
    Parameters:
    -----------
    pri : float
        PRI value
    
    Returns:
    --------
    str : Classification level
    """
    if pri >= 0.85:
        return "Excellent"
    elif pri >= 0.70:
        return "Good"
    elif pri >= 0.50:
        return "Moderate"
    else:
        return "Poor"

def calculate_pri_from_dict(vitals_dict):
    """
    Calculate PRI from dictionary
    
    Parameters:
    -----------
    vitals_dict : dict
        Dictionary containing vitals
    
    Returns:
    --------
    float : PRI value
    """
    return calculate_pri(
        vitals_dict.get('heart_rate'),
        vitals_dict.get('sbp'),
        vitals_dict.get('dbp'),
        vitals_dict.get('rr'),
        vitals_dict.get('spo2')
    )

# Import ML module (will be added if exists)
try:
    from .termux_ml import MOFNetPredictor, SimpleLinearRegression, SimpleDecisionTree
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    MOFNetPredictor = None
    SimpleLinearRegression = None
    SimpleDecisionTree = None

print(f"🏥 MOFNET v{__version__} loaded successfully")
if ML_AVAILABLE:
    print("🤖 ML Module loaded successfully")
