from setuptools import setup, find_packages

setup(
    name='mtamapper',
    version='0.0.1',
    author='Ryan Byrne',
    author_email='ryan@byrne.es',
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'mta-map=mtamapper.script:main',
        ]
    },
    install_requires = [
        'requests',
        'gtfs-realtime-bindings'
    ],
    package_data={'mtamapper':['lib/*','bin/*']},
    url='https://github.com/ryan-byrne/mta-map',
    license='LICENSE.txt',
    description='A Python Package for controlling an LED map of the MTA Subway system',
    long_description=open('README.md').read()
)