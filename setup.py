#!/usr/bin/env python

"""The setup script."""
from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()


parsed_requirements = parse_requirements("requirements.txt", session="workaround")

parsed_dev_requirements = parse_requirements("requirements_dev.txt", session="workaround")


requirements = [str(getattr(ir, "req", getattr(ir, "requirement", None))) for ir in parsed_requirements]
requirements_dev = [str(getattr(dr, "req", getattr(dr, "requirement", None))) for dr in parsed_dev_requirements]

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
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="pyscard-json-rpc",
    name="pyscard-json-rpc",
    packages=find_packages(include=["pyscard_json_rpc", "pyscard_json_rpc.*"]),
    test_suite="tests",
    tests_require=requirements_dev,
    url="https://github.com/namespace-ee/pyscard-json-rpc",
    version="0.1.0",
    zip_safe=False,
)
