from inspect import getsource
from IPython.display import display
from IPython.display import HTML

def psource(*functions):
    """Egy függvény forráskódját kinyomtató függvény."""
    source_code = '\n\n'.join(getsource(fn) for fn in functions)
    try:
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import PythonLexer
        from pygments import highlight

        display(HTML(highlight(source_code, PythonLexer(), HtmlFormatter(full=True))))

    except ImportError:
        print(source_code)