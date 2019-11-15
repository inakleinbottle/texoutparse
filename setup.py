import os

from setuptools import setup

DESCRIPTION = "Simple LaTeX log file parsing library."
here = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name='texoutparse',
    author='Sam Morley',
    author_email='sam@inakleinbottle.com',
    url="https://github.com/inakleinbottle/texoutparse",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['texoutparse'],
    version="1.1.0",
    tests_require=['pytest'],
    test_suite='tests',
    python_requires=">=3.6.0",
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ]

)
