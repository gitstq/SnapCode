#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapCode - Setup script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="snapcode",
    version="1.0.0",
    author="SnapCode Team",
    author_email="snapcode@example.com",
    description="📸 Lightweight Code Snapshot Management Tool - Zero dependencies CLI for managing code snapshots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/SnapCode",
    py_modules=["snapcode"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Version Control",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "snapcode=snapcode:main",
        ],
    },
    keywords="snapshot code backup version-control cli developer-tools",
)
