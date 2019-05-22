"""
Parser for LaTeX log files.
"""
import re
from collections import deque


class LogFileMessage:
    """
    Helper class for storing log file messages.

    Messages and attributes of the messages can be accessed and added using
    the item notation.
    """

    def __init__(self):
        self.info = {}
        self.context_lines = []

    def __str__(self):
        return '\n'.join(self.context_lines)

    def __getitem__(self, item):
        try:
            return self.info[item]
        except KeyError:
            raise KeyError(f'Item {item} was not found.')

    def __setitem__(self, key, value):
        self.info[key] = value


class _LineIterWrapper:
    """
    Wrapper around an iterable that allows peeking ahead to get context lines
    without consuming the iterator.
    """

    def __init__(self, iterable, ctx_lines):
        self.iterable = iter(iterable)
        self.cache = deque()
        self.ctx_lines = ctx_lines
        self.current = None

    def __next__(self):
        if self.cache:
            self.current = current = self.cache.popleft()
        else:
            self.current = current = next(self.iterable)
        return current

    def __iter__(self):
        return self

    def get_context(self):
        rv = [self.current] if self.current else []
        for _ in range(self.ctx_lines + 1 - len(rv)):
            try:
                next_val = next(self.iterable)
                self.cache.append(next_val)
                rv.append(next_val)
            except StopIteration:
                break
        return rv


class LatexLogParser:
    """
    Parser for LaTeX Log files.

    An LatexLogParser object can parse the log file or output of and generate
    lists of errors, warnings, and bad boxes described in the log. Each error.
    warning, or bad box is stored as a LogFileMessage in the corresponding
    list.
    """

    error = re.compile(
            r"^(?:! ((?:La|pdf)TeX|Package|Class)(?: (\w+))? [eE]rror(?: \(([\\]?\w+)\))?: (.*)|! (.*))"
            )
    warning = re.compile(
            r"^((?:La|pdf)TeX|Package|Class)(?: (\w+))? [wW]arning(?: \(([\\]?\w+)\))?: (.*)"
            )
    badbox = re.compile(
            r"^(Over|Under)full "
            r"\\([hv])box "
            r"\((?:badness (\d+)|(\d+(?:\.\d+)?pt) too \w+)\) (?:"
            r"(?:(?:in paragraph|in alignment|detected) "
            r"(?:at lines (\d+)--(\d+)|at line (\d+)))"
            r"|(?:has occurred while [\\]output is active [\[][\]]))"
            )

    def __init__(self, context_lines=2):
        self.warnings = []
        self.errors = []
        self.badboxes = []
        self.context_lines = context_lines

    def __str__(self):
        return (f"Errors: {len(self.errors)}, "
                f"Warnings: {len(self.warnings)}, "
                f"Badboxes: {len(self.badboxes)}")

    def process(self, lines):
        """
        Process the lines of a logfile to produce a report.

        Steps through each non-empty line and passes it to the process_line
        function.

        :param lines: Iterable over lines of log.
        """
        lines_iterable = _LineIterWrapper(lines, self.context_lines)

        # cache the line processor for speed
        process_line = self.process_line

        for i, line in enumerate(lines_iterable):
            if not line:
                continue
            err = process_line(line)
            if err is not None:
                err.context_lines = lines_iterable.get_context()

    def process_line(self, line):
        """
        Process a line in the log file and delegate to correct handler.

        Tests in turn matches to the badbox regex, warning regex, and
        then error regex. Once a match is found, the corresponding
        process function is called its result returned.

        :param line: Line to process
        :returns: LogFileMessage object or None
        """

        # Badboxes are probably most common, so match those first
        match = self.badbox.match(line)
        if match is not None:
            return self.process_badbox(match)

        # Now try warnings
        match = self.warning.match(line)
        if match is not None:
            return self.process_warning(match)

        # Now try errors
        match = self.error.match(line)
        if match is not None:
            return self.process_error(match)

        return None

    def process_badbox(self, match):
        """
        Process a badbox regex match and return the log message object.

        :param match: regex match object to process
        :return: LogFileMessage object
        """

        # Regex match groups
        # 0 - Whole match (line)
        # 1 - Type (Over|Under)
        # 2 - Direction ([hv])
        # 3 - Underfull box badness (badness (\d+))
        # 4 - Overfull box over size (\d+(\.\d+)?pt too \w+)
        # 5 - Multi-line start line (at lines (\d+)--)
        # 6 - Multi-line end line (--(d+))
        # 7 - Single line (at line (\d+))

        message = LogFileMessage()
        message['type'] = match.group(1)
        message['direction'] = match.group(2)

        # direction is either h or v
        message['by'] = match.group(3) or match.group(4)

        # single or multi-line
        if match.group(7) is not None:
            message['lines'] = (match.group(7), match.group(7))
        else:
            message['lines'] = (match.group(5), match.group(6))

        self.badboxes.append(message)
        return message

    def process_warning(self, match):
        """
        Process a warning regex match and return the log message object.

        :param match: regex match object to process
        :return: LogFileMessage object
        """

        # Regex match groups
        # 0 - Whole match (line)
        # 1 - Type ((?:La|pdf)TeX|Package|Class)
        # 2 - Package or Class name (\w*)
        # 3 - extra
        # 4 - Warning message (.*)

        message = LogFileMessage()
        message['type'] = type_ = match.group(1)

        if type_ == 'Package':
            # package name should be group 2
            message['package'] = match.group(2)
        elif type_ == 'Class':
            # class should be group 2
            message['class'] = match.group(2)
        elif match.group(2) is not None:
            # In any other case we want to record the component responsible for
            # the warning, if one is present.
            message['component'] = match.group(2)

        if match.group(3) is not None:
            message['extra'] = match.group(3)

        message['message'] = match.group(4)
        self.warnings.append(message)
        return message

    def process_error(self, match):
        """
        Process a warning regex match and return the log message object.

        :param match: regex match object to process
        :return: LogFileMessage object
        """

        # Regex match groups
        # 0 - Whole match (line)
        # 1 - Type (LaTeX|Package|Class)
        # 2 - Package or Class (\w+)
        # 3 - extra (\(([\\]\w+)\))
        # 4 - Error message for typed error (.*)
        # 5 - TeX error message (.*)

        message = LogFileMessage()
        if match.group(1) is not None:
            message['type'] = type_ = match.group(1)

            if type_ == 'Package':
                # Package name should be group 2
                message['package'] = match.group(2)
            elif type_ == 'Class':
                # Class name should be group 2
                message['class'] = match.group(2)
            elif match.group(2) is not None:
                message['component'] = match.group(2)

            if match.group(3) is not None:
                message['extra'] = match.group(3)


            message['message'] = match.group(4)
        else:
            message['message'] = match.group(5)

        self.errors.append(message)
        return message







