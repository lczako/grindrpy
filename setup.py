from setuptools import setup, find_packages

config = {
    'name': 'grindrpy',
    'description': 'Data preparation tool',
    'author': 'Lilla Czako',
    'author_email': 'lilla.czako@gmail.com',
    'version': '1.0',
    'packages': find_packages()
}

setup(**config)