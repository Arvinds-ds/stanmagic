from __future__ import print_function
from IPython.core.magic import Magics, cell_magic, magics_class

from IPython.utils.capture import capture_output

import pystan


def check_program(program):
    """
    Find the path of the given executable.
    """
    import os

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return "pystan"


@magics_class
class StanMagics(Magics):
    def __init__(self, shell):
        super(StanMagics, self).__init__(shell)

    @cell_magic
    def stan(self, line, cell):
        """
        Allow jupyter notebook cells to output stan code to file and compile it
        using stanc compiler in your path or pystan.stanc if no compiler is
        found in path. Output of compile is stored in "_stan_model object" or
        in an <object name> specified in -v <object_name> (e.g %%stan -f
        test.stan -v test)

        %%stan <variable_name>
        """
        args = " ".split(line.strip())
        if len(args) == 0:
            varname = "_stan_model"
        else:
            varname = args[0]

        print(
            f"Creating pystan model & assigning it to variable name {varname}."
        )

        with capture_output(display=False) as capture:
            try:
                _stan_model = pystan.StanModel(model_code=cell)
            except Exception:
                print(f"Error creating Stan model. Output:")
                print(capture)

        self.shell.user_ns[varname] = _stan_model
        print(f"StanModel now available as variable {varname}!")


def load_ipython_extension(ipython):
    ipython.register_magics(StanMagics)


def unload_ipython_extension(ipython):
    # ipython.user_global_ns.pop('_stan_vars', None)
    pass
