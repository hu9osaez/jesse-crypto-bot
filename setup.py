import os
from setuptools import setup, find_packages

from myapp import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = []

setup(
    name="My App",
    version=".".join(map(str, __version__)),
    description="",
    long_description=read('README.rst'),
    url='',
    license='MIT',
    author='Full Name',
    author_email='email@email.org',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    classifiers=[],
    install_requires=requirements,
    tests_require=[],
)
