from setuptools import setup
from pyesql import VERSION

setup(
    name='pyesql',
    version=VERSION,
    description='Python yesql clone',
    url='https://github.com/KMahoney/pyesql',
    packages=['pyesql'],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ]
)
