#!/usr/bin/env python

"""The setup script."""
from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()


def get_requirements(filename):
    """
    parse requirements.txt, ignore links, exclude comments
    """
    requirements = []
    for line in open(filename).readlines():
        # skip to next iteration if comment or empty line
        if line.startswith("#") or line == "" or line.startswith("http") or line.startswith("git"):
            continue
        # add line to requirements
        requirements.append(line)
    return requirements


setup(
    author="Namespace OÜ",
    author_email="info@namespace.ee",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="JSON RPC bindings for pyscard.",
    entry_points={
        "console_scripts": [
            "pyscard_json_rpc=pyscard_json_rpc.cli:main",
        ],
    },
    install_requires=get_requirements("requirements.txt"),
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="pyscard-json-rpc",
    name="pyscard-json-rpc",
    packages=find_packages(include=["pyscard_json_rpc", "pyscard_json_rpc.*"]),
    test_suite="tests",
    tests_require=get_requirements("requirements_dev.txt"),
    url="https://github.com/namespace-ee/pyscard-json-rpc",
    version="0.2.0",
    zip_safe=False,
)
