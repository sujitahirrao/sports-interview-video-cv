import os
from setuptools import find_packages, setup


# Utility function to read the README file.
# Used for the long_description.
def read(file_name):
    return open(os.path.join(os.path.dirname(__file__),
                             file_name)).read()


setup(
    name="interview_detection",
    package_dir={'': 'src'},
    packages=find_packages(where='src', exclude=["tests", "*visualization"]),
    version="0.1.0",
    author="Sujit Ahirrao",
    author_email="sujitahirrao3@gmail.com",
    description="Detect interview clips in the sports related videos",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    python_requires='>=3.6, <4',
)
