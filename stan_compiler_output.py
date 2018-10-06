from pygments import highlight as _highlight
from stan_lexer import StanLexer
from pygments.formatters import HtmlFormatter as _HtmlFormatter


class StanCode(str):
    def __init__(self, stan_code):
        super(StanCode, self).__init__()

    def __repr__(self):
        return self

    def _repr_html_(self):
        html = '<style type="text/css">{}</style>{}'.format(
            _HtmlFormatter().get_style_defs(".highlight"),
            _highlight(self, StanLexer(), _HtmlFormatter()),
        )
        return html


class StanMagicOutput:
    def __init__(self, model_name, stan_code, stan_file, cpp_file=None):
        if model_name is not None:
            self.model_name = model_name
        else:
            self.model_name = "Undefined"
        self.model_code = StanCode(stan_code)
        if stan_file is not None:
            self.model_file = stan_file
        else:
            self.model_file = "Undefined"
        self.cpp_file = cpp_file

    def __repr__(self):
        output = ""
        if self.model_file is not None:
            output += "model_file: {}\n".format(self.model_file)
        if self.model_name is not None:
            output += "model_name: {}\n".format(self.model_name)
        output += "model_code:\n"
        output += self.model_code
        return output

    def _repr_html_(self):
        html = ""
        if self.model_file is not None:
            html += (
                "<html><span><pre> model_file: <b>"
                + self.model_file
                + "</b></pre></span>"
            )
        if self.model_name is not None:
            html += (
                "<span><pre> model_name: <b>"
                + self.model_name
                + "</b></pre></span>"
            )

        html += "<span><pre><b> model_code :</b></pre></span>"

        html += '<style type="text/css">{}</style>{}'.format(
            _HtmlFormatter().get_style_defs(".highlight"),
            _highlight(self.model_code, StanLexer(), _HtmlFormatter()),
        )
        return html
