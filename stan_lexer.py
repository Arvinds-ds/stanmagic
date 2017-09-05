
import re

from pygments.util import shebang_matches
from pygments.lexer import Lexer, RegexLexer, bygroups, include, \
    combined, do_insertions
from pygments.token import Comment, String, Punctuation, Keyword, Name, \
    Operator, Number, Text, Generic

from pygments.lexers.agile import PythonLexer
from pygments.lexers import _scilab_builtins
import _stan_builtins

class StanLexer(RegexLexer):
    """Pygments Lexer for Stan models.

    The Stan modeling language is specified in the *Stan Modeling Language User's Guide and Reference Manual, v2.16.0*,
    
    """

    name = 'Stan'
    aliases = ['stan']
    filenames = ['*.stan']

    tokens = {
        'whitespace': [
            (r"\s+", Text),
        ],
        'comments': [
            (r'(?s)/\*.*?\*/', Comment.Multiline),
            # Comments
            (r'(//|#).*$', Comment.Single),
        ],
        'root': [
            # Stan is more restrictive on strings than this regex
            (r'"[^"]*"', String),
            # Comments
            include('comments'),
            # block start
            include('whitespace'),
            # Block start
            (r'(%s)(\s*)(\{)' %
             r'|'.join(('functions', 'data', r'transformed\s+?data',
                        'parameters', r'transformed\s+parameters',
                        'model', r'generated\s+quantities')),
             bygroups(Keyword.Namespace, Text, Punctuation)),
            # Assignment operators
            (r'(target)(\s*)([+][=])',
             bygroups(Keyword, Text, Operator)),
            # Reserved Words
            (r'(%s)\b' % r'|'.join(_stan_builtins.KEYWORDS), Keyword),
            # Truncation
            (r'T(?=\s*\[)', Keyword),
            # Data types
            (r'(%s)\b' % r'|'.join(_stan_builtins.TYPES), Keyword.Type),

            # Builtin
            (r'(%s)(?=\s*\()'
             % r'|'.join(_stan_builtins.FUNCTIONS
                         + _stan_builtins.DISTRIBUTIONS),
             Name.Builtin),
            # Reserved Words
            (r'(%s)\b' % r'|'.join(_stan_builtins.RESERVED), Keyword.Reserved),
            # user-defined functions
            (r'[A-Za-z]\w*(?=\s*\()]', Name.Function),
            # Regular variable names
            (r'[A-Za-z]\w*\b', Name),
            # Real Literals
            (r'-?[0-9]+(\.[0-9]+)?[eE]-?[0-9]+', Number.Float),
            (r'-?[0-9]*\.[0-9]*', Number.Float),
            # Integer Literals
            (r'-?[0-9]+', Number.Integer),
            # SLexer makes these tokens Operators.
            (r'<-|~', Operator),
            # Infix, prefix and postfix operators (and = )
            (r"\+|-|\.?\*|\.?/|\\|'|\^|==?|!=?|<=?|>=?|[|]{2}|&&|%|[?]|:", Operator),
            # Punctuation
            # needs to go after operators so | doesn't mask ||
            (r"[;,\[\]()|]", Punctuation),
            # Block delimiters
            (r'[{}]', Punctuation),
        ]
    }

    def analyse_text(text):
        if re.search(r'^\s*parameters\s*\{', text, re.M):
            return 1.0
        else:
            return 0.0
