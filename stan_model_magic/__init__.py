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
        Allow jupyter notebook cells create a pystan.StanModel object from
        Stan code in a cell that begins with %%stan. The pystan.StanModel
        gets assigned to a variable in the notebook's namespace, either
        named _stan_model (the default), or a custom name (specified
        by writing %%stan <variable_name>).
        """
        args = line.strip().split(' ')
        if len(args) == 0:
            varname = "_stan_model"
        else:
            varname = args[0]

        if not varname.isidentifier():
            raise ValueError(
                f"The variable name {varname} is not a valid variable name."
            )

        print(
            f"Creating pystan model & assigning it to variable "
            f"name \"{varname}\"."
        )

        with capture_output(display=False) as capture:
            try:
                _stan_model = pystan.StanModel(model_code=cell)
            except Exception:
                print(f"Error creating Stan model. Output:")
                print(capture)

        self.shell.user_ns[varname] = _stan_model
        print(f"StanModel now available as variable \"{varname}\"!")


def load_ipython_extension(ipython):
    ipython.register_magics(StanMagics)


def unload_ipython_extension(ipython):
    # ipython.user_global_ns.pop('_stan_vars', None)
    pass
