"""
Missing references tests
"""
import pytest

import texoutparse


@pytest.fixture
def parser():
    return texoutparse.LatexLogParser()


def test_missing_citation(parser):
    lines = [
        "LaTeX Warning: Citation `not present' on page 1 undefined on input line 7.",
        "BLANK",
        "BLANK"
    ]
    parser.process(lines)

    assert len(parser.missing_refs) == 1


def test_missing_reference(parser):
    lines = [
        "LaTeX Warning: Reference `not present' on page 1 undefined on input line 7.",
        "BLANK",
        "BLANK"
    ]
    parser.process(lines)

    assert len(parser.missing_refs) == 1
