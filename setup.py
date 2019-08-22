#!/usr/bin/env python3

import setuptools
import os
import time

with open('README.md', 'r') as README:

    setuptools.setup(
        name='jmatch',
        version=os.environ.get('CI_COMMIT_TAG', '0.0.1'),
        author='Jan Dillenberger',
        author_email='jdillenberger@uni-koblenz.de',
        long_description=README.read(),
        long_description_content_type='text/markdown',
        url='https://gitlab.rlp.net/jdillenberger/jmatch',
        packages=setuptools.find_packages(exclude=[]),
        python_requires='>=3.*',
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
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
