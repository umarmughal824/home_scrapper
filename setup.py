from setuptools import setup, find_packages

setup(
    name="web_scraper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "selenium",
    ],
    entry_points={
        'console_scripts': [
            'webscraper = hotel_scrapper.main:main',
        ],
    },
)
