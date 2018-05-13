from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()


setup(
    name='oevgk18_generator',
    version='0.0.1',
    description='Generate ÖV-Güteklassen 2018',
    long_description=readme,
    author='Jonas Matter, Robin Suter',
    author_email='robin@robinsuter.ch',
    url='https://github.com/public-transport-quality-grades/oevgk18-generator',
    license="MIT License",
    packages=find_packages(exclude=('tests')),
    install_requires=['Shapely', 'Rtree', 'geojson', 'records'],
    entry_points={
        'console_scripts': [
            'oevgk18_generator=generator.__main__:main'
        ]
    }
)
