from pip.req import parse_requirements
from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
version = open('version', 'r').read()
install_reqs = parse_requirements(os.path.join(here, 'requirements.txt'))
install_requires = [str(ir.req) for ir in install_reqs]


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
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['spcchart=spcchart:main']
    }
)
