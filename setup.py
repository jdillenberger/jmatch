#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md', 'r') as README:

    setup(
        name='jMatch',
        version='0.1',
        author='Jan Dillenberger',
        author_email='jdillenberger@uni-koblenz.de',
        long_description=README.read(),
        long_description_content_type='text/markdown',
        url='https://gitlab.rlp.net/jdillenberger/jmatch',
        packages=find_packages(exclude=[]),
        python_requires='>=3.*',
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Linux",
        ],
        entry_points={
            'console_scripts': [
                'jmatch=jmatch:main',
            ],
        },
        project_urls={
            'Bug Reports': 'https://gitlab.rlp.net/jdillenberger/jmatch/issues/new',
            'Source': 'https://gitlab.rlp.net/jdillenberger/jmatch',
        }
    )
