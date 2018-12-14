import setuptools

from kasi import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

version = __version__

setuptools.setup(
    name="kasi",
    version=version,
    author="Jaroslav Lhotak",
    author_email="jarda@lhotak.net",
    description="A simple socket cache server",
    python_requires=">=3.4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lhotakj/Kasi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Environment :: Web Environment",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP :: Session",
        "License :: OSI Approved :: Apache License 2.0",
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
    ],
)