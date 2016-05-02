#!/usr/bin/env python3

from setuptools import setup

version = '0.0.3'

setup(name='makejsonapiclient',
    version=version,
    description="Simple python utility to build a python client library for interfacing with a JSON API",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    entry_points={
        'console_scripts': [
            'makejsonapiclient = makejsonapiclient.__main__:main',
            ]
        },
    keywords='python http json management',
    author='Taylor C. Richberger <tcr@absolute-performance.com>',
    author_email='tcr@absolute-performance.com',
    url='https://github.com/Taywee/makejsonapiclient',
    download_url='https://github.com/Taywee/makejsonapiclient',
    license='MIT',
    packages=['makejsonapiclient'],
    include_package_data=False,
    zip_safe=False,
    )
