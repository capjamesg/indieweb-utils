import setuptools
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="indieweb-utils",
    version="0.9.1",
    author="capjamesg",
    author_email="jamesg@jamesg.blog",
    description="Utilities to aid the implementation of various IndieWeb specifications and functionalities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/capjamesg/indieweb-utils",
    project_urls={
        "Bug Tracker": "https://github.com/capjamesg/indieweb-utils/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "mf2py==1.1.2",
        "requests",
        "beautifulsoup4==4.10.0",
        "lxml==4.9.1",
        "pyjwt==2.4.0",
        "jwt==1.3.1",
        "granary",
        "Pillow"
    ],
)
