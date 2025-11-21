from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")
setup(
    name="magic-extractor",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "pyfiglet",
        "tqdm",
        "termcolor"
    ],
    entry_points={
        "console_scripts": [
            "magic-extractor=magic_extractor.main:main"
        ]
    },
    author="Elm4g3k",
    description="Discover Your Target Automatically",
    python_requires=">=3.8"
)
