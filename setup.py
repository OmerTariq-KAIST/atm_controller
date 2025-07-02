"""
Setup script for ATM Controller package
"""
from setuptools import setup, find_packages

setup(
    name="atm-controller",
    version="1.0.0",
    description="ATM controller implementation Demo for Bear Robotics Assessment",
    author="Omer Tariq",
    author_email="omertariq2000@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
)