import setuptools
from setuptools import find_packages
import re
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")

with open("./src/indieweb_utils/__init__.py", "r") as f:
    content = f.read()
    # from https://www.py4u.net/discuss/139845
    version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content).group(1)

setuptools.setup(
    name="indieweb-utils",
    version=version,
    author="capjamesg",
    author_email="jamesg@jamesg.blog",
    description=" Building blocks for IndieWeb applications.",
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
        "Pillow",
        "granary",
        "http_message_signatures",
        "python-jose"
    ]
)
