import setuptools
from setuptools import find_packages
import re

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("./src/indieweb_utils/__init__.py", "r") as f:
    content = f.read()
    # from https://www.py4u.net/discuss/139845
    version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content).group(1)

setuptools.setup(
    name="indieweb-utils",
    version=version,
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
        "mf2py",
        "requests",
        "beautifulsoup4",
        "lxml",
        "pyjwt",
        "granary",
        "Pillow"
    ],
)
