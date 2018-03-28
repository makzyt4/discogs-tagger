from distutils.core import setup

setup(
    name="discogs-tagger",
    version="0.1.0",
    packages=['discogstagger'],
    entry_points={
        'console_scripts': [
            'discogs-tagger = discogstagger.__main__:main'
        ]
    },
    description='Discogs album tags downloader',
    author='Maksymilian Zytkiewicz',
    author_email='maksymilian.zytkiewicz@gmail.com',
    url='https://github.com/makzyt4/discogs-tagger',
    keywords=['music', 'webcrawling'],
    license=open('LICENSE').read(),
    long_description=open('README.md').read()
)
