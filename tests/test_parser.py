from textwrap import dedent

import pytest

import texoutparse


@pytest.fixture
def parser():
    return texoutparse.LatexLogParser()





