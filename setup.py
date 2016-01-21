from distutils.core import setup

setup(
    name='ExerciseDB',
    version='1.0',
    description='ExerciseDB',
    author='Craig Ellis',
    author_email='ellis.cr@husky.neu.edu',
    url='https://www.python.org/sigs/distutils-sig/',
    packages=['templates',
              'templates.users',
              'templates.utils']
)
