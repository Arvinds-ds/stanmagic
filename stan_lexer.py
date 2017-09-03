
import re

from pygments.util import shebang_matches
from pygments.lexer import Lexer, RegexLexer, bygroups, include, \
    combined, do_insertions
from pygments.token import Comment, String, Punctuation, Keyword, Name, \
    Operator, Number, Text, Generic

from pygments.lexers.agile import PythonLexer
from pygments.lexers import _scilab_builtins
from pygments.lexers import _stan_builtins

class StanLexer(RegexLexer):
    """Pygments Lexer for Stan models.

    The Stan modeling language is specified in the *Stan Modeling Language User's Guide and Reference Manual, v2.16.0*,
    
    """

    name = 'Stan'
    aliases = ['stan']
    filenames = ['*.stan']

    tokens = {
        'whitespace' : [
            (r"\s+", Text),
            ],
        'comments' : [
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
            (r'(%s)(\s*)({)' %
             r'|'.join(('data', r'transformed\s+?data',
                        'parameters', r'transformed\s+parameters',
                        'model', r'generated\s+quantities')),
             bygroups(Keyword.Namespace, Text, Punctuation)),
            # Reserved Words
            (r'(%s)\b' % r'|'.join(_stan_builtins.KEYWORDS), Keyword),
            # Truncation
            (r'T(?=\s*\[)', Keyword),
            # Data types
            (r'(%s)\b' % r'|'.join(_stan_builtins.TYPES), Keyword.Type),
            # Punctuation
            (r"[;:,\[\]()]", Punctuation),
            # Builtin
            (r'(%s)(?=\s*\()'
             % r'|'.join(_stan_builtins.FUNCTIONS
                         + _stan_builtins.DISTRIBUTIONS),
             Name.Builtin),
            # Special names ending in __, like lp__
            (r'[A-Za-z][A-Za-z0-9_]*__\b', Name.Builtin.Pseudo),
            (r'(%s)\b' % r'|'.join(_stan_builtins.RESERVED), Keyword.Reserved),
            # Regular variable names
            (r'[A-Za-z][A-Za-z0-9_]*\b', Name),
            # Real Literals
            (r'-?[0-9]+(\.[0-9]+)?[eE]-?[0-9]+', Number.Float),
            (r'-?[0-9]*\.[0-9]*', Number.Float),
            # Integer Literals
            (r'-?[0-9]+', Number.Integer),
            # Assignment operators
            # SLexer makes these tokens Operators.
            (r'<-|~', Operator),
            # Infix and prefix operators (and = )
            (r"\+|-|\.?\*|\.?/|\\|'|==?|!=?|<=?|>=?|\|\||&&", Operator),
            # Block delimiters
            (r'[{}]', Punctuation),
            ]
        }

    def analyse_text(text):
        if re.search(r'^\s*parameters\s*\{', text, re.M):
            return 1.0
        else:
            return 0.0
