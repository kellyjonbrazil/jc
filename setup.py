import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='jc',
    version='1.7.5',
    author='Kelly Brazil',
    author_email='kellyjonbrazil@gmail.com',
    description='This tool serializes the output of popular command line tools and filetypes to structured JSON output.',
    install_requires=[
        'ifconfig-parser>=0.0.5',
        'ruamel.yaml>=0.15.0',
        'xmltodict>=0.12.0'
    ],
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    url='https://github.com/kellyjonbrazil/jc',
    packages=setuptools.find_packages(),
    include_package_data=True,
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
