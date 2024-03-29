from setuptools import setup

setup(
    name='dip',
    version='1.1.1',
    packages=['dip'],
    url='https://github.com/Soren98/dip',
    license='Unlicense',
    author='Søren',
    author_email='sorenthedesolate@gmail.com',
    description='A discord bot that manages instances of the board game Diplomacy(1959).',
    install_requires=['discord.py', 'pillow'],
    requires_python='>=3.6.0'
)
