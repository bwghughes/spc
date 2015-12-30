from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
version = open('version', 'r').read()
install_requires = [
    "numpy==1.7.1",
    "pygal==1.4.6",
    "shortuuid==0.4",
    "wsgiref==0.1.2",
]


setup(name='spcchart',
    version=version,
    description="SPC Charts For Humans",
    long_description='Read more here at: https://statistical-process-control-charts.readthedocs.org/en/latest/',
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='statistics, spc, chart, tool, process control',
    author='Ben Hughes',
    author_email='bwghughes@gmail.com',
    url='spc.io',
    license='BSD',
    packages=['spcchart'],
    include_package_data=True,
    zip_safe=False,
    setup_requires=['numpy==1.7.1'],
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['spcchart=spcchart:main']
    }
)
