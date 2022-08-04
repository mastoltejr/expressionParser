import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="expressionParser",                     # This is the name of the package
    version="1.0.0",                        # The initial release version
    author="Michael Stolte",                     # Full name of the author
    description="Math Expression Parser that works with [ + - * / ^ // ! ] operators, constants [ pi ], functions [ exp, log, ln ], strings [\"testString\"], and [variables] out of the box and can be expanded to cover more use cases!",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.10.0',                # Minimum version requirement of the package
    py_modules=["expressionParser"],             # Name of the python package
    package_dir={'':'.'},     # Directory of the source code of the package
    install_requires=["python-dateutil >= 2.8.2"]                     # Install other dependencies if any
)