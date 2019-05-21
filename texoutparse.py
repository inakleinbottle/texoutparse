#
#
"""
Parser for LaTeX log files.
"""
import re


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
        return ('Message('
                + ', '.join(f'{k}: {v}' for k, v in self.info.items())
                + ')')

    def __getitem__(self, item):
        try:
            self.info['item']
        except KeyError:
            raise KeyError(f'Item {item} was not found.')

    def __setitem__(self, key, value):
        self.info[key] = value


class LatexLogParser:
    """
    Parser for LaTeX Log files.
    """

    error = re.compile(
            r"^(?:! (LaTeX|Package|Class)( \w+)? Error: (.*)|! (.*))"
            )
    warning = re.compile(
            r"^((?:La|pdf)TeX|Package|Class)( \w+)? Warning: (.*)"
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

        :param lines: Iterable over lines of log
        """

        # cache the line processor for speed
        process_line = self.process_line

        # Add one to context lines to get correct slices
        ctx_lines = self.context_lines + 1

        for i, line in enumerate(lines):
            err = process_line(line)

    def process_line(self, line):
        """
        Process a line in the log file and delegate to correct handler.

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
        # 3 - Warning message (.*)

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

        message['message'] = match.group(3)
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
        # 3 - Error message for typed error (.*)
        # 4 - TeX error message (.*)

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

            message['message'] = match.group(3)
        else:
            message['message'] = match.group(4)

        self.errors.append(message)
        return message







