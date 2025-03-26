from setuptools import setup, find_packages

setup(
    name="martyrs-foundation",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "PyQt6",
    ],
    entry_points={
        'console_scripts': [
            'martyrs-foundation=app.main:main',
        ],
    },
) 