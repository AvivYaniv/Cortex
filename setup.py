
print("Setup is starting...")

from setuptools import setup, find_packages

setup(
    name = 'Cortex',
    version = '0.1.0',
    author = 'Aviv Yaniv',
    description = 'Brain machine interface with extreme flexibility and scalability',
    packages = find_packages(),
    install_requires = ['click', 'flask', 'docker'],
    tests_require = ['pytest', 'pytest-cov'],
)
