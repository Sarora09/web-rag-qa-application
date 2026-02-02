from setuptools import setup, find_packages

with open("requirements.txt") as r:
    requirements = r.read().splitlines()

setup(
    name = "WEB-RAG-QA-APPLICATION",
    version = "0.1",
    author = "Sapan",
    packages = find_packages(),
    install_requires = requirements,
)