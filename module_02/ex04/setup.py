from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'How to create a package in python.'

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="my-minipack", 
        version=VERSION,
        author="Eduard vendrell",
        author_email="evendrel@student.42barcelona.com",
        license="MIT",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        installer="pip",
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Intended Audience :: Students",
            "Topic :: Education",
            "Topic :: HowTo",
            "Topic :: Package",
            "License :: MIT",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
        ]
)
