from setuptools import setup
from __init__ import VERSION


setup(name='zot',
      version=VERSION,
      description='zotero command-line interface',
      author='Ben Morris',
      author_email='ben@bendmorris.com',
      url='https://github.com/hourchallenge/zot',
      packages=['zot'],
      package_dir={
                'zot':''
                },
      entry_points={
        'console_scripts': [
            'zot = zot.zot:main',
        ],
      },
      )
