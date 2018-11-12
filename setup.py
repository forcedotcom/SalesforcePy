import os.path
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as fh:
    install_requires = fh.readlines()

with open(os.path.join(os.path.dirname(__file__), 'requirements-dev.txt')) as fh:
    tests_require = fh.readlines()

setuptools.setup(
    name='SalesforcePy',
    version='1.0.3',
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
    tests_require=tests_require)
