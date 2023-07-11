
from setuptools import setup
  
setup(
    name='DQR_Data',
    version='0.1',
    description='A python library for cryptocurrency trading for Binance and Deribit',
    author='DAOQuantResearch',
    author_email='DQR-contact@proton.me',
    packages=['DQR_Data'],
    install_requires=[
        'requests',
        'pandas',
        'websocket-client',
        'aiohttp',
    ],
)