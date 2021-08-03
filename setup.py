from setuptools import find_packages
from setuptools import setup

# setup.py generated by https://github.com/hexiro/pykager

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open('requirements.txt', 'r') as req_file:
    requirements = [l for l in req_file.read().splitlines() if l and not l.startswith('#')]

packages = ['pykager'] + [('pykager.' + x) for x in find_packages(where='pykager')]

setup(
    name='pykager',
    version='1.0.0rc1',
    description='setup.py generator with smart defaults',
    author='Hexiro',
    author_email='realhexiro@gmail.com',
    url='https://github.com/Hexiro/pykager',
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=requirements,
    zip_safe=True,
    packages=packages,
    entry_points={'console_scripts': ['pykager = pykager.__main__:main']},
)
