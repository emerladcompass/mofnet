# mofnet - Medical MOF Prediction

A Python package for predicting Multi-Organ Failure (MOF) using Patient Resilience Index (PRI).

## Quick Start

```bash
# Install
pip install git+https://github.com/emerladcompass/mofnet.git

# Use
import mofnet

# Calculate PRI
pri = mofnet.calculate_pri(80, 120, 80, 16, 98)
classification = mofnet.classify_pri_level(pri)
```

Features

· Patient Resilience Index (PRI) calculation
· Real-time monitoring capabilities
· Clinical classification of risk levels
· Simple and intuitive API

Author

Samir Baladi (@emerladcompass)
Interdisciplinary AI Researcher
📧 emerladcompass@gmail.com
🔗 ORCID: 0009-0003-8903-0029

License

MIT License - See LICENSE file for details.
