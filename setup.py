from setuptools import setup, find_packages
from pathlib import Path

#######################################
# Prepare list of compiled extensions #
#######################################

extensions = []


#########
# Setup #
#########

version_file = Path(__file__).parent / 'xsuite/_version.py'
dd = {}
with open(version_file.absolute(), 'r') as fp:
    exec(fp.read(), dd)
__version__ = dd['__version__']

setup(
    name='xsuite',
    version=__version__,
    description='Integrated suite for particle accelerator simulations',
    long_description='Integrated suite for particle accelerator simulations',
    author='R. De Maria, G. Iadarola et al.',
    packages=find_packages(),
    ext_modules=extensions,
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
    entry_points={
        'console_scripts': ['xsuite-prebuild=xsuite.cli:main'],
    },
)
