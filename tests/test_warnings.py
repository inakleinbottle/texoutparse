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

    assert len(parser.warnings) == 1


def test_latex_font_warning(parser):
    lines = [
        "LaTeX Font Warning: Font shape `OT1/cmr/bx/sc' undefined",
        "(Font) using `OT1/cmr/bx/n' instead on input line 9."
    ]
    parser.process(lines)

    assert len(parser.warnings) == 1


def test_latex_undefined_reference_warning(parser):
    lines = [
        "LaTeX Warning: Reference `undefined refr' on page 1 undefined on input line 17.",
        " BLANK",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.warnings) == 1


def test_class_warning(parser):
    lines = [
        "Class article Warning: Unknown option `foo'.",
        " BLANK",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.warnings) == 1