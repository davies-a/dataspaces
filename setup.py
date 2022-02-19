from setuptools import find_packages, setup

setup(
    name="dataspaces",
    version="0.0.1",
    author="Alex Davies",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "pydantic",
        "docker",
    ],
    entry_points={
        "console_scripts": [
            "dspace = dspace.dspace:cli",
        ],
    },
    extras_require={
        "test": [
            "pytest",
            "pytest-mock",
        ]
    },
    test_suite="pytest",
)
