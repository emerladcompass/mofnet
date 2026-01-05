from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mofnet",
    version="1.0.2",
    author="Samir Baladi",
    author_email="emerladcompass@gmail.com",
    description="Multi-Organ Failure Network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emerladcompass/mofnet",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
