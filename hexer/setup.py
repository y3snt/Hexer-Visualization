from setuptools import setup, find_packages

setup(
    name='hexer',
    version='0.0.1',
    packages=find_packages('hexer', exclude=('tests*')),
    author='Magdalena Doleśniak',
)