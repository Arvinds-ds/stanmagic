from __future__ import print_function
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
import shlex
import uuid
import tempfile
import os

from stan_compiler_output import StanMagicOutput


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

    return 'pystan'

def print_compile_success(variable_name, stan_file, model_name, model_code):
    print('-'*79)
    print('Model compiled successfully. Output stored in {0} object.'.format(variable_name))
    print('Type {0} in a cell to see a nicely formatted code output in a notebook'.format(variable_name))
    print('     ' + '^'*len(variable_name))
    print('Access model compile output properties')
    print('{0}.model_file -> Name of stan_file [{1}]'.format(variable_name,
                                                                        stan_file))
    print('{0}.model_name -> Name of stan model [{1}]'.format(variable_name,
                                                                        model_name))
    code_sample = model_code[:20].replace('\n',' ')
    print('{0}.model_code -> Model code [{1} ....]'.format(variable_name,code_sample ))

@magics_class
class StanMagics(Magics):
    def __init__(self,shell):
        super(StanMagics,self).__init__(shell)

    @cell_magic
    def stan(self,line, cell):
        '''
        Allow jupyter notebook cells to output stan code to file and compile it using
        stanc compiler in your path or pystan.stanc if no compiler is found in path.
        Output of compile is stored in "_stan_model object" or  in an <object name>
        specified in -v <object_name> (e.g %%stan -f test.stan -v test)
        %%stan
        - Saves the cell code to a string. The code string can be accessed via
        _stan_model.model_code or <object_name>.model_code
        (if you specify -v <object_name> option)
        %%stan -f <stan_file_name>
        - Saves the cell code to a file specified in <stan_file_name>. The file name
        can also be accessed in _stan_model.model_file or in
        <object_name>.model_file (if you specify -v <object_name> option)
        %%stan -v <object_name> [default: _stan_model]
          stan magic currently outputs a StanMagicOutput object in default _stan_model object.
           -v allows you to specify an alternate compile output object name, so that
           you can use specified object name instead of "_stan_model".
           This is useful if you have multiple %%stan model cells. Cuurently the output object
           exposes 3 attributes (model_name, model_code, model_file)
           [_stan_model | <object_name>].model_file -> Name of stan_file
           [_stan_model | <object_name>].model_name -> Name of stan model [None]
           [_stan_model | <object_name>].model_code -> Model code
        %%stan -f <stan_file_name> --save_only
        - Saves the cell code to a file specified in <stan_file_name>. Skips
        compile step
        %%stan -f <stan_file_name> -o <cpp_file_name>
        - Saves the cell code to a file specified in <stan_file_name> and outputs the
        compiled cpp file to the file name specified by <cpp_file_name>
        %% stan -f <stan_file_name> --allow_undefined
        - passes the --allow_undefined argument to stanc compiler
        %%stan --stanc <stanc_compiler> [default: stanc in $PATH or pystan.stanc]
        - Saves the cell code to a file specified in <stan_file_name> and compiles
        using the stan compiler specified in <stanc_compiler>.
        Optionally, if you specify --stanc pystan, it uses pystan.stanc compiler.
        If you want to use specific stanc compiler
        use this option (e.g %%stan -f binom.stan --stanc "~/cmdstan-2.16.0/bin/stanc")
        '''
        _stan_vars = {}
        __stan_code_str__ = None
        __stan_file__ = None
        __model_name__ = None

        ip = get_ipython()
        args = shlex.split(line.strip())
        options = {k: True if v.startswith('-') else v
               for k,v in zip(args, args[1:]+["--"]) if k.startswith('-')}
        source_filename = options.get('-f',None)
        output_filename = options.get('-o',None)
        variable_name = options.get('-v','_stan_model')
        allow_undefined = options.get('--allow_undefined',False)
        save_only = options.get('--save_only',False)

        if save_only is True:
            if source_filename is None:
                print("Need to specify stan file name (-f) for --save_only")
                return
            else:
                with open(source_filename, 'w') as f:
                    f.write(cell)
                _stan_vars['stan_file'] = source_filename
                print("File {0} saved..Skipping Compile".format(source_filename))
                return

        compiler_location = options.get('--stanc', check_program('stanc'))
        if not (isinstance(compiler_location, str)):
            print("Pls specify a location for stanccompiler or \
                   specify '--stanc pystan' to use pystan.stanc compiler")
            return
        temp_dir = tempfile.gettempdir()

        if compiler_location is None or compiler_location=='pystan':
            print("Using pystan.stanc compiler..")
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
            __stan_code_str__ = cell
            __stan_file__ = source_filename
            __model_name__ = model_name

        with open(source_filename, 'w') as f:
            f.write(cell)
        if compiler_location is None or compiler_location=='pystan':
            try:
                import pystan as _pystan
                try:
                     out = _pystan.stanc(source_filename,verbose=True)
                except Exception as e:
                     print(e)
                     return
            except ImportError:
                print("Ensure stan command line (stanc) is installed and in your \
                   PATH or pystan is installed or specify compiler path using --stanc \
                   (e.g. %% stan -f model.stan --stanc ./bin/stanc")
                return

        else:
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
            compile_output = ip.getoutput(compile_str)
            print('\n'.join(compile_output))

        _stan_vars[variable_name] = StanMagicOutput(__model_name__,__stan_code_str__,
                    __stan_file__);
        ip.user_global_ns[variable_name] = _stan_vars[variable_name]
        print_compile_success(variable_name,__stan_file__,__model_name__, __stan_code_str__)


def load_ipython_extension(ipython):
    ipython.register_magics(StanMagics)


def unload_ipython_extension(ipython):
    #ipython.user_global_ns.pop('_stan_vars', None)
    pass
