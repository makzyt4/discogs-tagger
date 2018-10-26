from distutils.core import setup

setup(
    name="discogs-tagger",
    version="0.1.3",
    packages=['discogstagger'],
    entry_points={
        'console_scripts': [
            'discogs-tagger = discogstagger.__main__:main'
        ]
    },
    install_requires=[
        'beautifulsoup4',
        'fuzzywuzzy',
        'mutagen',
        'requests',
        'urllib3'
    ],
    description='Discogs album tags downloader',
    author='Maksymilian Zytkiewicz',
    author_email='maksymilian.zytkiewicz@gmail.com',
    url='https://github.com/makzyt4/discogs-tagger',
    keywords=['music', 'webcrawling'],
    license=open('LICENSE').read(),
    long_description=open('README.md').read()
)
