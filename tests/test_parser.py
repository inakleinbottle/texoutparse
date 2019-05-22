"""
Generic tests

The tests in this file are for generic tests for the parser and associated objects..
"""
import pytest

import texoutparse


@pytest.fixture
def parser():
    return texoutparse.LatexLogParser()


def test_string_rep_of_parser_no_items(parser):
    assert str(parser) == 'Errors: 0, Warnings: 0, Badboxes: 0'


def test_string_rep_of_parser_error(parser):
    parser.errors.append(1)
    assert str(parser) == 'Errors: 1, Warnings: 0, Badboxes: 0'


def test_string_rep_of_parser_warning(parser):
    parser.warnings.append(1)
    assert str(parser) == 'Errors: 0, Warnings: 1, Badboxes: 0'


def test_string_rep_of_parser_badbox(parser):
    parser.badboxes.append(1)
    assert str(parser) == 'Errors: 0, Warnings: 0, Badboxes: 1'


def test_parse_no_messages(parser):
    lines = [
        " BLANK",
        " BLANK",
        "",
        " BLANK",
    ]
    parser.process(lines)

    assert len(parser.errors) == 0
    assert len(parser.warnings) == 0
    assert len(parser.badboxes) == 0


@pytest.fixture
def wrapper():
    return texoutparse._LineIterWrapper(range(10), 2)


def test_iterable_wrapper_get_context(wrapper):
    assert wrapper.get_context() == [0, 1, 2]
    assert next(wrapper) == 0
    assert list(wrapper.cache) == [1, 2]


def test_iterable_wrapper_context_at_last_entry(wrapper):
    full = list(wrapper)  # Consume the iterable
    assert full == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert wrapper.get_context() == [9]



@pytest.fixture
def message():
    message = texoutparse.LogFileMessage()
    message.context_lines = [
        "context line 1",
        "context line 2",
        "context line 3",
    ]
    return message


def test_log_file_message_string_format(message):
    assert str(message) == "context line 1\ncontext line 2\ncontext line 3"
