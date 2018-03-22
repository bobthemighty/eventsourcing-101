from setuptools import setup, find_packages

setup(
    name='mongobasket',
    url='https://github.com/bobthemighty/eventsourcing-101',
    description='Code samples for the eventsouricng 101 talk',
    packages=find_packages('.'),
    entry_points={
        'console_scripts': ['basket=mongobasket.cli:main']
    }
)
