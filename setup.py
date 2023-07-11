
from setuptools import setup

setup(
    name='DQR_Data',
    version='0.1.3',
    description='A python library for cryptocurrency trading for Binance and Deribit',
    author='DAOQuantResearch',
    author_email='DQR-contact@proton.me',
    packages=['DQR_Data'],
    url="https://github.com/DAOQuantResearch/data_package/tree/release_v1",
    project_urls={
        'Source': 'https://github.com/DAOQuantResearch/data_package/tree/release_v1',
    },
    install_requires=[
        'requests',
        'pandas',
        'websocket-client',
        'aiohttp',
    ],
)