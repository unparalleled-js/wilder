from codecs import open
from os import path

from setuptools import find_packages
from setuptools import setup

here = path.abspath(path.dirname(__file__))

about = {}
with open(path.join(here, "src", "wilder", "__version__.py"), encoding="utf8") as fh:
    exec(fh.read(), about)

with open(path.join(here, "README.md"), "r", "utf-8") as f:
    readme = f.read()

setup(
    name="wilder",
    version=about["__version__"],
    url="https://github.com/unparalleled-js/wilder",
    project_urls={
        "Issue Tracker": "https://github.com/unparalleled-js/wilder/issues",
        "Source Code": "https://github.com/unparalleled-js/wilder",
    },
    description="Wilder music production tools.",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*<4",
    install_requires=[
        "click>=7.1.2",
        "Flask==1.1.2",
        "PyInquirer>=1.0.3",
        "python-vlc>=3.0.11115",
        "requests>=2.25.1",
    ],
    extras_require={
        "dev": [
            "flake8==3.8.3",
            "pytest==4.6.11",
            "pytest-cov==2.10.0",
            "pytest-mock==2.0.0",
            "tox>=3.17.1",
        ]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    entry_points={"console_scripts": ["wild=wilder.cli.main:cli"]},
)
