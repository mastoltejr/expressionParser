import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # This is the name of the package
    name="callableExpressionParser",
    version="1.0.0",                        # The initial release version
    author="Michael Stolte",                     # Full name of the author
    description="Math Expression Parser that works with [ + - * / ^ // ! ] operators, constants [ pi ], functions [ exp, log, ln ], strings [\"testString\"], and [variables] out of the box and can be expanded to cover more use cases!",
    # Long description read from the the readme file
    long_description=long_description,
    long_description_content_type="text/markdown",
    # List of all python modules to be installed
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    # Minimum version requirement of the package
    python_requires='>=3.10.0',
    # Name of the python package
    py_modules=["callableExpressionParser"],
    package_dir={'': '.'},     # Directory of the source code of the package
    # Install other dependencies if any
    install_requires=["python-dateutil >= 2.8.2"]
)
