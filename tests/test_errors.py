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


def test_undefined_control_seq_tex_error(parser):
    lines = [
        "! Undefined control sequence.",
        "l.6 \dtae",
        "{December 2004}"
    ]
    parser.process(lines)

    assert len(parser.errors) == 1


def test_too_many_braces_tex_error(parser):
    lines = [
        "! Too many }'s.",
        "l.6 \\date December 2004}"
    ]
    parser.process(lines)

    assert len(parser.errors) == 1


def test_missing_math_mode_tex_error(parser):
    lines = [
        "! Missing $ inserted",
        " BLANK",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 1


def test_package_error(parser):
    lines = [
        "! Package babel Error: Unknown option `latin'. Either you misspelled it",
        "(babel)                or the language definition file latin.ldf was not found.",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 1


def test_pdftex_error(parser):
    lines = [
        "! pdfTeX error (\\pdfsetmatrix): Unrecognized format..",
        " BLANK",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 1


def test_class_error(parser):
    lines = [
        "! Class article Error: Unrecognized argument for \\macro.",
        " BLANK",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 1


