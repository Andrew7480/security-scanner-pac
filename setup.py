from setuptools import setup, find_packages

setup(
    name="secscan",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "secscan=scanner.main:main"
        ]
    },
)
