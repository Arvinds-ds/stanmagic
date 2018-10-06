# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

readme = open("README.md").read()

setup(
    name="jupyterstan",
    version="0.0.1",
    description="Magics for defining stan code in notebooks.",
    long_description=readme,
    author="Jan Freyberg",
    author_email="jan.freyberg@gmail.com",
    url="https://github.com/janfreyberg/jupyterstan",
    packages=find_packages(),
    install_requires=["ipython", "pystan"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: IPython",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
