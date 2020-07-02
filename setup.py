import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()


install_requires = ['requests>=2.21.0', ]

tests_require = [
    'responses==0.10.1',
    'coverage==5.1',
    'pytest==5.4.3',
    'python-coveralls==2.9.1',
    'pytest-flake8==1.0.6',
    'flake8==3.8.2',
    'wheel==0.33.4',
]


setuptools.setup(
    name='SalesforcePy',
    version='2.0.0',
    description='An absurdly simple package for making Salesforce Rest API requests',
    url='https://github.com/forcedotcom/SalesforcePy',
    author='Aaron Caffrey',
    author_email='acaffrey@salesforce.com',
    license='BSD',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=tests_require
)
