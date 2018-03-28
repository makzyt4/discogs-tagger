from distutils.core import setup

setup(
    name="DiscogsTagger",
    version="0.1 beta",
    packages=['discogstagger'],
    entry_points={
        'console_scripts': [
            'discogs-tagger = discogstagger.__main__:main'
        ]
    },
    license='MIT License',
    long_description=open('README.md').read()
)
