from setuptools import setup

setup(
    name='ciscot7',
    version=1,
    description='Cisco Type 7 Password Decrypter',
    author='theevilbit',
    url='https://github.com/theevilbit/ciscot7',
    license='MIT',
    py_modules=[
        'ciscot7'
    ],
    python_requires='>=3.0.0',
    entry_points={
        'console_scripts': [
            'ciscot7 = ciscot7:main'
        ]
    }
)
