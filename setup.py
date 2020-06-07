import setuptools

description = "Written in python, for checking reference lists in systematic reviews and literature reviews, helps with reference list searching both backward&forward by extracting references and creating search queries, ranks articles by relevance to improve screening efficiency, download full-text pdf of research articles in batch."

with open("README.md","r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="refchaser",
    version='0.0.2',
    authpr='Dingqi Zhang',
    author_email='zhangdingqi1998@gmail.com',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DQ-Zhang/refchaser.git',
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ],
    python_requires='>=3'
)