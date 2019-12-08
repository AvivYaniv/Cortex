from setuptools import setup, find_packages


setup(
    name = 'Cortex',
    version = '0.1.0',
    author = 'Aviv Yaniv',
    description = 'Advanced System Design Project',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest', 'pytest-cov'],
)