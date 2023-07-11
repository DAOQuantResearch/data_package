
from setuptools import setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()  
setup(
    name='DQR_Data',
    version='0.1.1',
    description='A python library for cryptocurrency trading for Binance and Deribit',
    long_description=long_description,    
    long_description_content_type="text/markdown",
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