# TexOutParse
Simple output/log file parsing library for LaTeX builds. 

LaTeX log files are notoriously unstructured and there is a wide variance in the style
and content of messages.
Messages can be roughly characterised as an error, an warning, a bad box, or info.
Packages and classes can also generate messages and, while there are template macros
 for producing such messages, no structure is
enforced on the messages.

Many LaTeX editors provide a log file parser that runs automatically on building
the document.
A summary of the errors, warnings, and bad boxes is usually displayed to the user.
There does not seem to be any library or tool for parsing log files separate from these editors.

## Installalation
The library can be installed via Pip
```sh
pip install texoutparse
```

## Usage
The main class provided by this library is `LaTexLogParser`, which is used to parse
the log file and collect the statistics. 
```python
from texoutparse import LatexLogParser

parser = LatexLogParser()
with open('sample.log') as f:
    parser.process(f)
```
The `parser` object contains lists of errors, warnings, and bad boxes, each described by an 
`LogFileMessage` object. Both objects provide a `__str__` method that prints a summary of the
error in the case of `LatexLogParser` and the raw lines in the case of `LogFileMessage`.
```
>>> print(parser)
Errors: 1, Warnings: 1, Badboxes:1

>>> print(parser.errors[0])
! Undefined control sequence.
l.6 \dtae
{December 2004}
```            

## Contributing
 1. Fork it. (https://github.com/inakleinbottle/fork)
 2. Create a feature branch. (`git checkout -b feature/name`)
 3. Commit your changes. (`git commit -m 'add some feature'`)
 4. Push the branch to Github. (`git push origin feature/name`)
 5. Create a pull request.

## Meta
Sam Morley - [inakleinbottle.com](https://inakleinbottle.com) - admin@inakleinbottle.com

Distributed under the MIT license. See `LICENSE` for more information.
 
 ## Release History
 - 1.0. Initial release