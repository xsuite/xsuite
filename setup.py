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
    version='0.3.0',
    description='Integrated suite for particle accelerator simulation',
    url='https://github.com/xsuite/xsuite',
    author='Giovanni Iadarola, Riccardo De Maria',
    packages=find_packages(),
    ext_modules = extensions,
    install_requires=[
        'numpy>=1.0',
        'xobjects',
        'xtrack',
        'xfields',
        'xpart'
        ]
    )
