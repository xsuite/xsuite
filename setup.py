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
    version='0.4.0',
    description='Integrated suite for particle accelerator simulations',
    long_description='Integrated suite for particle accelerator simulations',
    author='R. De Maria, G. Iadarola et al.',
    packages=find_packages(),
    ext_modules = extensions,
    install_requires=[
        'numpy>=1.0',
        'xobjects',
        'xtrack',
        'xfields',
        'xpart',
        'xdeps'
        ],
    url='https://xsuite.readthedocs.io/',
    license='Apache 2.0',
    download_url="https://pypi.python.org/pypi/xsuite",
    project_urls={
            "Bug Tracker": "https://github.com/xsuite/xsuite/issues",
            "Documentation": 'https://xsuite.readthedocs.io/',
            "Source Code": "https://github.com/xsuite/xsuite",
        },
    )
