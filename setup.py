from setuptools import setup

setup(name='wpscraper',
      version='0.1',
      description='WordPress Site Recent Articles Scraper',
      packages=['wpscraper'],
      install_requires=[
            'requests',
            'pandas',
            'sqlalchemy',
      ],
      author='Faye Hall',
      author_email='fayedaihall@mac.com',
      url='https://github.com/fayehall',
      zip_safe=False)
