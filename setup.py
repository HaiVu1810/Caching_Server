from setuptools import setup

setup(
    name='caching-server',
    version='1.0',
    py_modules=['caching_server', 'Fetchinghandle', 'Socket_server'],
    entry_points={
        'console_scripts': [
            'caching-server=caching_server:main', # Nó sẽ gọi hàm main() trong file caching_server.py
        ],
    },
)