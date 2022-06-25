from setuptools import setup, find_packages
import os
import re


# auto-updating version code stolen from orbitize
def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
                       open(project + '/__init__.py').read())
    return result.group(1)

setup(
    name='FRAPP',
    version=get_property('__version__', 'FRAPP'),
    packages=find_packages(),
    description='FRAPP (Font-Facilitated Reading for Arxiv PDF Publications)',
    url='https://github.com/mpgalleg/FRAPP',
    author='MGG, QH, PP',
    keywords='ArXiv Reading Accessibility',
    install_requires=get_requires()
)
