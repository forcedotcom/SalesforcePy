from setuptools import setup
setup(name='SalesforcePy',
      version='1.0.0',
      description='An absurdly simple package for making Salesforce Rest API requests',
      url='https://github.com/salesforce/SalesforcePy',
      author='Aaron Caffrey',
      author_email='acaffrey@salesforce.com',
      license='MIT',
      packages=['SalesforcePy'],
      zip_safe=False,
      package_dir={'SalesforcePy': 'src'},
      install_requires=['requests', 'pytest', 'responses', 'coverage', 'python-coveralls'],
      tests_require=['pytest', 'responses']
      )
