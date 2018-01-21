from distutils.core import setup

setup(name='pyriver',
      version='0.0.1.3',
      description='River client.',
      url='http://github.com/ptbrodie/pyriver',
      author='Patrick Brodie',
      author_email='ptbrodie@gmail.com',
      install_requires=[
        'beautifulsoup4==4.6.0',
        'redis==2.10.6',
        'requests==2.18.4',
        'schedule==0.5.0',
        'sqlalchemy==1.2.1',
      ],
      scripts=['./river'])
