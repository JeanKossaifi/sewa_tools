try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

config = {
    'description': 'Simple utility package to help with the SEWA data.',
    'author': 'Jean Kossaifi',
    'author_email': 'jean [dot] kossaifi [at] gmail [dot] com',
    'version': '0.1',
    'install_requires': ['numpy', 'scipy', 'pandas'],
    'packages': find_packages(),
    'scripts': [],
    'name': 'sewa_tools'
}

setup(**config)
