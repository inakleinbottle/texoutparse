"""
Bad box tests

The tests in this file should test bad boxes occurring in log files. These
should be genuine badbox messages from LaTeX log files, possibly including
BLANK lines in the lines iterable.
"""
import pytest

import texoutparse


@pytest.fixture
def parser():
    return texoutparse.LatexLogParser()


def test_underfull_vbox_while_output_active(parser):
    lines = [
        "Underfull \\vbox (badness 1234) has occurred while \\output is active []"
        " BLANK"
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 0
    assert len(parser.warnings) == 0
    assert len(parser.badboxes) == 1

    err = parser.badboxes[0]

    assert err.context_lines == lines
    assert err['type'] == 'Under'
    assert err['direction'] == 'v'
    assert err['by'] == '1234'


def test_underfull_vbox_detected_at(parser):
    lines = [
        "Underfull \\vbox (badness 10000) detected at line 19",
        "[]",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 0
    assert len(parser.warnings) == 0
    assert len(parser.badboxes) == 1

    err = parser.badboxes[0]

    assert err.context_lines == lines
    assert err['type'] == 'Under'
    assert err['direction'] == 'v'
    assert err['by'] == '10000'
    assert err['lines'] == ('19', '19')


def test_underfull_hbox_at_lines(parser):
    lines = [
        "Underfull \\hbox (badness 1234) in paragraph at lines 9--10",
        " BLANK",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 0
    assert len(parser.warnings) == 0
    assert len(parser.badboxes) == 1

    err = parser.badboxes[0]

    assert err.context_lines == lines
    assert err['type'] == 'Under'
    assert err['direction'] == 'h'
    assert err['by'] == '1234'
    assert err['lines'] == ('9', '10')



def test_overfull_vbox_while_output_active(parser):
    lines = [
        "Overfull \\vbox (19.05511pt too high) has occurred while \\output is active []",
        " BLANK",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 0
    assert len(parser.warnings) == 0
    assert len(parser.badboxes) == 1

    err = parser.badboxes[0]

    assert err.context_lines == lines
    assert err['type'] == 'Over'
    assert err['direction'] == 'v'
    assert err['by'] == '19.05511pt'


def test_overfull_hbox_on_line(parser):
    lines = [
        "Overfull \\hbox (54.95697pt too wide) in paragraph at lines 397--397",
        " BLANK",
        " BLANK"
    ]
    parser.process(lines)

    assert len(parser.errors) == 0
    assert len(parser.warnings) == 0
    assert len(parser.badboxes) == 1

    err = parser.badboxes[0]

    assert err.context_lines == lines
    assert err['type'] == 'Over'
    assert err['direction'] == 'h'
    assert err['by'] == '54.95697pt'
    assert err['lines'] == ('397', '397')

