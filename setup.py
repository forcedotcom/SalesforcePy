import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='SalesforcePy',
    version='1.0.2',
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
    install_requires=['requests', 'pytest',
                    'responses', 'coverage'],
    tests_require=['pytest', 'responses']
)
