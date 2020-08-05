import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='jc',
    version='1.13.3',
    author='Kelly Brazil',
    author_email='kellyjonbrazil@gmail.com',
    description='Converts the output of popular command-line tools and file-types to JSON.',
    install_requires=[
        'ruamel.yaml>=0.15.0',
        'xmltodict>=0.12.0',
        'Pygments>=2.3.0'
    ],
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    url='https://github.com/kellyjonbrazil/jc',
    packages=setuptools.find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    entry_points={
        'console_scripts': [
            'jc=jc.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
    ]
)
