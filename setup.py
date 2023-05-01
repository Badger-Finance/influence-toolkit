import pathlib

from setuptools import find_packages
from setuptools import setup

with open("requirements.txt", "r") as f:
    requirements = list(map(str.strip, f.read().split("\n")))[:-1]

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
    name="influence-toolkit",
    install_requires=requirements,
    author="PETROVSKA",
    author_email="petrovska@badger.com",
    description="Helper methods for influence calculations",
    long_description=README,
    keywords=["influence-toolkit"],
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    version="0.0.1",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    license="MIT",
    url="https://github.com/Badger-Finance/influence-toolkit",
)
