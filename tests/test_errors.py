"""
Error tests

The tests in this file should test errors occurring in log files. These
should be genuine error messages from LaTeX log files, possibly including
BLANK lines in the lines iterable.
"""
import pytest

import texoutparse


@pytest.fixture
def parser():
    return texoutparse.LatexLogParser()


def test_package_not_found_error(parser):
    lines = [
        "! LaTeX Error: File `foobar.sty' not found.",
        " BLANK",
        " BLANK",
    ]

    parser.process(lines)

    assert len(parser.errors) == 1
    assert len(parser.warnings) == 0
    assert len(parser.badboxes) == 0

    err = parser.errors[0]

    assert err['message'] == "File `foobar.sty' not found."
    assert err.context_lines == lines


def test_undefined_control_seq_tex_error(parser):
    lines = [
        "! Undefined control sequence.",
        "l.6 \\dtae",
        "{December 2004}"
    ]
    parser.process(lines)

    assert len(parser.errors) == 1
    assert len(parser.warnings) == 0
    assert len(parser.badboxes) == 0

    err = parser.errors[0]

    assert err.context_lines == lines
    assert err['message'] == "Undefined control sequence."


def test_too_many_braces_tex_error(parser):
    lines = [
        "! Too many }'s.",
        "l.6 \\date December 2004}"
    ]
    parser.process(lines)

    assert len(parser.errors) == 1
    assert len(parser.warnings) == 0
    assert len(parser.badboxes) == 0

    err = parser.errors[0]

    assert err.context_lines == lines
    assert err['message'] == "Too many }'s."


def test_missing_math_mode_tex_error(parser):
    lines = [
        "! Missing $ inserted",
        " BLANK",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 1
    assert len(parser.warnings) == 0
    assert len(parser.badboxes) == 0

    err = parser.errors[0]

    assert err.context_lines == lines
    assert err['message'] == "Missing $ inserted"


def test_package_error(parser):
    lines = [
        "! Package babel Error: Unknown option `latin'. Either you misspelled it",
        "(babel)                or the language definition file latin.ldf was not found.",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 1
    assert len(parser.warnings) == 0
    assert len(parser.badboxes) == 0

    err = parser.errors[0]

    assert err.context_lines == lines
    assert err['type'] == 'Package'
    assert err['package'] == 'babel'
    assert err['message'] == "Unknown option `latin'. Either you misspelled it"


def test_pdftex_error(parser):
    lines = [
        "! pdfTeX error (\\pdfsetmatrix): Unrecognized format..",
        " BLANK",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 1
    assert len(parser.warnings) == 0
    assert len(parser.badboxes) == 0

    err = parser.errors[0]

    assert err.context_lines == lines
    assert err['type'] == 'pdfTeX'
    assert err['extra'] == '\\pdfsetmatrix'
    assert err['message'] == "Unrecognized format.."


def test_class_error(parser):
    lines = [
        "! Class article Error: Unrecognized argument for \\macro.",
        " BLANK",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 1
    assert len(parser.warnings) == 0
    assert len(parser.badboxes) == 0

    err = parser.errors[0]

    assert err.context_lines == lines
    assert err['type'] == 'Class'
    assert err['class'] == 'article'
    assert err['message'] == "Unrecognized argument for \\macro."


