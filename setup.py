from distutils.core import setup

setup(name='ddp',
      version='1.0',
      description='Distributed Data Protocol (DDP) server',
      author='Colin Ligertwood',
      author_email='colin@brainbits.ca',
      packages=['ddp'],
      install_requires=[
          'tornado',
          'sockjs-tornado',
          'meteor-ejson',
      ]
     )
