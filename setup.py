import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="jc",
    version="0.1",
    author="Kelly Brazil",
    description="This tool serializes the output of popular command line tools to structured JSON output.",
    install_requires=[
        collections,
        ifconfigparser,
        json
    ],
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='~=3.4',
    url="https://github.com/kellyjonbrazil/jc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
