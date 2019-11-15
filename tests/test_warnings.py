"""
Warning tests

The tests in this file should test warnings occurring in log files. These
should be genuine warning messages from LaTeX log files, possibly including
BLANK lines in the lines iterable.
"""
import pytest

import texoutparse


@pytest.fixture
def parser():
    return texoutparse.LatexLogParser()


def test_package_warning(parser):
    lines = [
        "Package hyperref Warning: Draft mode on.",
        " BLANK",
        " BLANK",
    ]
    parser.process(lines)

    assert len(parser.errors) == 0
    assert len(parser.warnings) == 1
    assert len(parser.badboxes) == 0

    err = parser.warnings[0]

    assert err.context_lines == lines
    assert err['type'] == 'Package'
    assert err['package'] == 'hyperref'
    assert err['message'] == 'Draft mode on.'


def test_latex_font_warning(parser):
    lines = [
        "LaTeX Font Warning: Font shape `OT1/cmr/bx/sc' undefined",
        "(Font) using `OT1/cmr/bx/n' instead on input line 9."
    ]
    parser.process(lines)

    assert len(parser.errors) == 0
    assert len(parser.warnings) == 1
    assert len(parser.badboxes) == 0

    err = parser.warnings[0]

    assert err.context_lines == lines
    assert err['type'] == 'LaTeX'
    assert err['component'] == 'Font'
    assert err['message'] == "Font shape `OT1/cmr/bx/sc' undefined"


@pytest.mark.skip
def test_latex_undefined_reference_warning(parser):
    lines = [
        "LaTeX Warning: Reference `undefined refr' on page 1 undefined on input line 17.",
        " BLANK",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 0
    assert len(parser.warnings) == 1
    assert len(parser.badboxes) == 0

    err = parser.warnings[0]

    assert err.context_lines == lines
    assert err['type'] == 'LaTeX'
    assert err['message'] == "Reference `undefined refr' on page 1 undefined on input line 17."


def test_class_warning(parser):
    lines = [
        "Class article Warning: Unknown option `foo'.",
        " BLANK",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 0
    assert len(parser.warnings) == 1
    assert len(parser.badboxes) == 0

    err = parser.warnings[0]

    assert err.context_lines == lines
    assert err['type'] == 'Class'
    assert err['class'] == 'article'
    assert err['message'] == "Unknown option `foo'."