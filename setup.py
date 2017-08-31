# -*- coding: utf-8 -*-

from setuptools import setup

readme = open('README.rst').read()

setup(
    name='stanmagic',
    version='0.0.1',
    description='An extension for Jupyter that help to run Stan code in '
                'your interactive session.',
    long_description=readme,
    author='Aravind S',
    author_email='arvindxxxx@gmail.com',
    url='https://github.com/arvinds-ds/stanmagic',
    py_modules=(
        'stanmagic',
    ),
    install_requires=(
        'ipython',
    ),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
