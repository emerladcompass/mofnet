#!/data/data/com.termux/files/usr/bin/bash
# update_setup.sh

cd ~/storage/downloads/mofnet

echo "🔄 تحديث إعدادات المشروع..."
echo ""

# 1. تحديث setup.py
cat > setup.py << 'EOF'
from setuptools import setup, find_packages

# قراءة الوصف
with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()

setup(
    name="mofnet",
    version="1.0.2",
    author="Samir Baladi",
    author_email="emerladcompass@gmail.com",
    description="Multi-Organ Failure Network - Clinical Prediction System",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/emerladcompass/mofnet",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
    ],
)
EOF

echo "✅ تم تحديث setup.py"

# 2. إنشاء ملف __version__.py
cat > mofnet/__version__.py << 'EOF'
__version__ = "1.0.2"
__author__ = "Samir Baladi"
__email__ = "emerladcompass@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2024, MOFNet Project"
EOF

echo "✅ تم إنشاء __version__.py"

# 3. إعادة التثبيت
pip install -e . --force-reinstall

echo "✅ تم إعادة التثبيت"
echo ""
echo "📦 معلومات الحزمة:"
python3 -c "import mofnet; print(f'اسم: {mofnet.__name__}'); print(f'إصدار: {getattr(mofnet, \"__version__\", \"غير محدد\")}')"
