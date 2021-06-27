import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dlm-lector",
    version="1.0.0",
    author="dicenlosmedios",
    author_email="visualizadordecontexto@gmail.com",
    description="lector de dicenlosmedios ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miglesias91/dlm-lector",
    project_urls={
        "Bug Tracker": "https://github.com/miglesias91/dlm-lector/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
)