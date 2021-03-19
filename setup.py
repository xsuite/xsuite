from setuptools import setup, find_packages, Extension

#######################################
# Prepare list of compiled extensions #
#######################################

extensions = []


#########
# Setup #
#########

setup(
    name='xsuite',
    version='0.0.0',
    description='Integrated suite for particle acclerator simulation'
    url='https://github.com/xsuite/xsuite',
    author='Giovanni Iadarola',
    packages=find_packages(),
    ext_modules = extensions,
    install_requires=[
        'numpy>=1.0',
        ]
    )
