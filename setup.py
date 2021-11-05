# coding: utf-8

from setuptools import setup, find_packages

NAME = "ts-ids-validator"
VERSION = "0.9.1"

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

# Read Requirements
with open("./requirements.txt", "r") as req_file:
    requirements = req_file.read()
    requirements = requirements.splitlines()
    requirements = [
        req
        for req in requirements
        if req and req[0].isalpha()
    ]

setup(
    name=NAME,
    version=VERSION,
    description="Python utility for validating IDS",
    author="tetrascience",
    author_email="developers@tetrascience.com",
    url="https://github.com/tetrascience/ts-ids-validator",
    project_urls={
        "Tetra Developer Site": "https://developers.tetrascience.com",
    },
    keywords=[],
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
    license='Apache License 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)