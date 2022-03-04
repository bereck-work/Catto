from glob import glob
from os.path import splitext, basename

from setuptools import setup, find_packages

setup(
    name="catto",
    version="1.0.0",
    description="A simple command line tool that downloads cute animals images of your choice.",
    packages=find_packages("src"),
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "click",
        "loguru",
        "requests",
        "questionary",
        "pyfiglet",
        "colorama",
        "pillow",
        "alive-progress",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    entry_points={
        "console_scripts": [
            "catto=catto:main_command_interface",
        ],
    },
)
