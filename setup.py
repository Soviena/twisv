from setuptools import setup, find_packages
from twisv.version import versioning
setup(
    name="twisv",
    version=versioning.ver,
    author="Soviena",
    author_email="rovino.rs@gmail.com",
    description="Stream anime from kaa.si and sync with anilist",
    packages=find_packages(),
    url="https://github.com/Soviena/twisv",
    keywords=[
        "twitter",
        "downloader",
        "cli",
        "scraper",
        "twitter-downloader"
    ],
    install_requires=[
        "platformdirs",
        "requests",
    ],
    entry_points={
        'console_scripts': ['twisv=twisv.main:twisv']
    }
)