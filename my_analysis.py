import mofnet

patients = [
    {"name": "John", "hr": 85, "sbp": 125, "dbp": 82, "rr": 18, "spo2": 97},
    {"name": "Jane", "hr": 105, "sbp": 145, "dbp": 95, "rr": 22, "spo2": 93},
]

for p in patients:
    pri = mofnet.calculate_pri(p["hr"], p["sbp"], p["dbp"], p["rr"], p["spo2"])
    print(f"{p['name']}: PRI={pri:.3f} -> {mofnet.classify_pri_level(pri)}")
