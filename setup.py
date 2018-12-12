from setuptools import setup                                                                                 
from setuptools import find_packages

#version = __import__('merlin').VERSION

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='combinatorial-game-ai',
      version=version,
      description='Different agents for playing combinatorial games.',
      long_description=readme(),
      classifiers=[
        'Programming Language :: Python :: 3',
      ],  
      keywords='machine deep reinforcement learning chess ai agent',
      url='https://github.com/BayBenj/chess',
      author='Benjamin Bay',
      author_email='benjamin.bay@gmail.com',
      license='LLNL',
      packages=find_packages(),
      install_requires=[
        'matplotlib',
        'numpy',
        'scipy',
        'sqlalchemy',
        'parse',
        'pyDOE'
      ],  
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      include_package_data=True,
      zip_safe=False)

