from distutils.core import setup

setup(
    name="discogs-tagger",
    version="0.1.1",
    packages=['discogstagger'],
    entry_points={
        'console_scripts': [
            'discogs-tagger = discogstagger.__main__:main'
        ]
    },
    install_requires=[
        'beautifulsoup4==4.6.0',
        'fuzzywuzzy==0.16.0',
        'mutagen==1.40.0',
        'requests==2.17.3',
        'urllib3==1.22'
    ],
    description='Discogs album tags downloader',
    author='Maksymilian Zytkiewicz',
    author_email='maksymilian.zytkiewicz@gmail.com',
    url='https://github.com/makzyt4/discogs-tagger',
    keywords=['music', 'webcrawling'],
    license=open('LICENSE').read(),
    long_description=open('README.md').read()
)
