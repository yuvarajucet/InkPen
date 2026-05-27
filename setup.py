"""Setup configuration for InkPen"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="InkPen",
    version="1.0.0",
    author="InkPen Team",
    description="A Windows overlay drawing application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/InkPen",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyQt5>=5.15.0",
        "Pillow>=9.0.0",
        "numpy>=1.21.0",
    ],
    extras_require={
        "dev": [
            "pyinstaller>=5.0.0",
            "pytest>=7.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "inkpen=app:main",
        ],
    },
)
