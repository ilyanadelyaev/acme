import os
from setuptools import setup


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='acme-neuro-api',
    version='1.0',
    packages=[
        'acme',
        #
        'acme.tools',
        #
        'acme.lib',
        'acme.lib.rest',
        #
        'acme.neuro',
        'acme.neuro.api',
        'acme.neuro.api.view',
    ],
    include_package_data=True,
    description='ACME Neuro API',
    url='https://github.com/ilyanadelyaev/acme',
    author='Ilya Nadelyaev',
    author_email='--@--.--',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
