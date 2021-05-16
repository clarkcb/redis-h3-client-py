from setuptools import setup
from redis_h3_client import __version__

setup(name='redis-h3-client-py',
      version=__version__,
      description='A client of redis server with H3 module loaded',
      url='https://github.com/clarkcb/redis-h3-client-py.git',
      author='Cary Clark',
      author_email='clarkcb@gmail.com',
      install_requires=['redis'],
      license='MIT',
      packages=['redis_h3_client'],
      python_requires='>=3',
      tests_require=[])
