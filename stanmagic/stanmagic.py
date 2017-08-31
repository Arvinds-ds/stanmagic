from __future__ import print_function
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
import shlex
import uuid
import tempfile
import os


_stan_vars = {}

def check_program(program):
    '''
    Find the path of the given executable.
    '''
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

    return None

@magics_class
class StanMagics(Magics):

    @cell_magic
    def stan(self,line, cell):
        '''
        Allow jupyter notebook cells to output stan code to file and compile it using
        stanc compiler.
        %%stan
        - Saves the cell code to a string. The code string can be accessed via
        _stan_vars['stan_code']
        %%stan -f <stan_file_name>
        - Saves the cell code to a file specified in <stan_file_name>. The file name
        can also be accessed in _stan_vars['stan_file'] generated in local namespace
        %%stan -f <stan_file_name> --save_only
        - Saves the cell code to a file specified in <stan_file_name>. Skips
        compile step
        %%stan -f <stan_file_name> -o <cpp_file_name>
        - Saves the cell code to a file specified in <stan_file_name> and outputs the
        compiled cpp file to the file name specified by <cpp_file_name>
        %% stan -f <stan_file_name> --allow_undefined
        - passes the --allow_undefined argument to stanc compiler
        %%stan -f <stan_file_name> --stanc <stanc_compiler>
        - Saves the cell code to a file specified in <stan_file_name> and compiles
        using the stan compiler specified in <stanc_compiler>. By default, it uses
        stanc compiler in your path. If your path does not have the stanc compiler,
        use this option (e.g %%stan binom.stan --stanc "~/cmdstan-2.16.0/bin/stanc")
        '''
        __stan_code_str__ = None
        __stan_file__ = None
        __model_name__ = None

        ip = get_ipython()
        args = shlex.split(line.strip())
        options = {k: True if v.startswith('-') else v
               for k,v in zip(args, args[1:]+["--"]) if k.startswith('-')}
        source_filename = options.get('-f',None)
        output_filename = options.get('-o',None)
        allow_undefined = options.get('--allow_undefined',False)
        save_only = options.get('--save_only',False)

        if save_only is True:
            if source_filename is None:
                print("Need to specify stan file name (-f) for --save_only")
                return
            else:
                with open(source_filename, 'w') as f:
                    f.write(cell)
                print("File {0} saved..Skipping Compile".format(source_filename))
                return

        compiler_location = options.get('--stanc', check_program('stanc'))
        temp_dir = tempfile.gettempdir()

        if compiler_location is None:
            print("Ensure stan command line (stanc) is installed and in your \
                   PATH or specify compiler path using --stanc \
                   (e.g. %% stan -f model.stan --stanc ./bin/stanc")
            return
        else:
            print("Using stanc compiler: ", compiler_location)

        # We define the source and executable filenames.
        if source_filename is None:
            temp_name= str(uuid.uuid4())
            source_filename = os.path.join(temp_dir,'anon_' + \
                                temp_name + '.stan')
            output_filename = os.path.join(temp_dir,'anon_' + temp_name + \
                                 '_model.cpp')
            model_name = 'anon_' +temp_name + '_model'
            __stan_code_str__ = cell
            __stan_file__ = None
            __model_name__ = None
        else:
            __stan_file = source_filename
            model_name = source_filename.split('.')
            if len(model_name) > 1:
                model_name = '_'.join(model_name[:-1])
            else:
                model_name = ''.join(model_name)
            model_name = model_name + '_model'
            __stan_code_str__ = None
            __stan_file__ = source_filename
            __model_name__ = model_name

        with open(source_filename, 'w') as f:
            f.write(cell)

        compile_str = compiler_location

        if output_filename is not None:
            compile_str = compile_str + ' --o=' + output_filename
        else:
            compile_str = compile_str + ' --o=' + \
                              os.path.join(temp_dir,str(uuid.uuid4()) +'.cpp')

        if allow_undefined is True:
            compile_str = compile_str + ' --allow_undefined '

        compile_str = compile_str + ' ' + source_filename

        print(compile_str)
        compile = ip.getoutput(compile_str)
        _stan_vars['stan_file'] = __stan_file__
        _stan_vars['stan_code'] = __stan_code_str__
        _stan_vars['model_name'] = __model_name__

        print('\n'.join(compile))

def load_ipython_extension(ipython):
    ipython.user_global_ns['_stan_vars'] = _stan_vars
    ipython.register_magics(StanMagics)


def unload_ipython_extension(ipython):
    ipython.user_global_ns.pop('_stan_vars', None)
