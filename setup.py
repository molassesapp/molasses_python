#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "requests==2.24.0",
    "APScheduler==3.6.3"
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', 'responses']

setup(
    author="James Hrisho",
    author_email='admin@molasses.app',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="python SDK for Molasses - feature flags as a service",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='molasses, feature flags, feature toggles',
    name='molasses',
    packages=find_packages(include=['molasses', 'molasses.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/molassesapp/molasses_python',
    version='0.1.3',
    zip_safe=False,
)
