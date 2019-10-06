from setuptools import find_packages, setup

__version__ = "0.0.1"

setup(
    name="frail",
    version=__version__,
    packages=find_packages(),
    author="Jules Léné",
    description="Search french train prices.",
    long_description=open("README.md").read(),
    install_requires=["requests", "pendulum"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
    ],
)
