import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Grab version from version.py
__version__ = ""
exec(open('openai_kernel/version.py').read())

setuptools.setup(
    name="openai_kernel",
    version=__version__,
    author="Oak City Labs",
    author_email="team@oakcity.io",
    description="OpenAI jupyter kernel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={"openai_kernel": ["*.json"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=[
        "openai>=0.27.4,<1",
        "metakernel>=0.29.4,<1"
    ],
)