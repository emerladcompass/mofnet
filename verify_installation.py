#!/usr/bin/env python3
"""
Verify MOFNet installation
"""

import sys
import mofnet

print("🔬 MOFNet Installation Verification")
print("=" * 40)

checks = []

# Check 1: Import
try:
    import mofnet
    checks.append(("Import", "✅", "Module imported successfully"))
except ImportError as e:
    checks.append(("Import", "❌", f"Failed: {e}"))

# Check 2: Version
try:
    version = mofnet.__version__
    checks.append(("Version", "✅", f"v{version}"))
except AttributeError:
    checks.append(("Version", "❌", "Version not found"))

# Check 3: Core functions
functions_to_check = ['calculate_pri', 'classify_pri_level']
for func in functions_to_check:
    if hasattr(mofnet, func):
        checks.append((f"Function: {func}", "✅", "Available"))
    else:
        checks.append((f"Function: {func}", "❌", "Missing"))

# Check 4: Actual calculation
try:
    pri = mofnet.calculate_pri(80, 120, 80, 16, 98)
    checks.append(("PRI Calculation", "✅", f"Result: {pri}"))
except Exception as e:
    checks.append(("PRI Calculation", "❌", f"Error: {e}"))

# Check 5: Classification
try:
    classification = mofnet.classify_pri_level(0.85)
    checks.append(("Classification", "✅", f"Example: {classification}"))
except Exception as e:
    checks.append(("Classification", "❌", f"Error: {e}"))

# Display results
print("\nResults:")
print("-" * 40)
for check, status, message in checks:
    print(f"{status} {check}: {message}")

# Summary
success_count = sum(1 for _, status, _ in checks if status == "✅")
total_count = len(checks)

print(f"\n📊 Summary: {success_count}/{total_count} checks passed")
if success_count == total_count:
    print("🎉 MOFNet is fully operational!")
else:
    print("⚠️ Some issues detected")

print(f"\nPython: {sys.version}")
