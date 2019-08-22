#!/usr/bin/env python3

import setuptools
import os
import time

with open('README.md', 'r') as README:

    setuptools.setup(
        name='jMatch',
        version=os.environ.get('CI_COMMIT_TAG', os.environ.get('CI_COMMIT_SHORT_SHA', str(time.time()))),
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
