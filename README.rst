stanmagic
====================

An extension for `Jupyter <https://jupyter.org>`__ that help to run
Stan code in your interactive session.


Installation
------------
Ensure you have the STAN compiler (stanc) installed on your platform. Instructions
can be found at https://github.com/stan-dev/cmdstan

Ensure that stanc is in your path or you need to pass the compiler path
specifically as outlined below

Install ``stanmagic`` using
`pip <http://www.pip-installer.org/>`__:

::

    $ pip install git+https://github.com/Arvinds-ds/stanmagic.git

Usage
-----
See sample notebook https://github.com/Arvinds-ds/stanmagic/blob/master/StanMagic-Help.ipynb
for usage details

`%%stan`
  Saves the cell code to a string. The code string can be accessed via
  _stan_vars['stan_code']

`%%stan -f <stan_file_name>`
  Saves the cell code to a file specified in <stan_file_name>. The file name
  can also be accessed in _stan_vars['stan_file'] generated in local namespace

`%%stan -f <stan_file_name> --save_only`
  Saves the cell code to a file specified in <stan_file_name>. Skips
  compile step

`%%stan -f <stan_file_name> -o <cpp_file_name>`
  Saves the cell code to a file specified in <stan_file_name> and outputs the
  compiled cpp file to the file name specified by <cpp_file_name>

`%% stan -f <stan_file_name> --allow_undefined`
  passes the --allow_undefined argument to stanc compiler

`%%stan -f <stan_file_name> --stanc <stanc_compiler>`
  Saves the cell code to a file specified in <stan_file_name> and compiles
  using the stan compiler specified in <stanc_compiler>. By default, it uses
  stanc compiler in your path. If your path does not have the stanc compiler,
  use this option (e.g %%stan binom.stan --stanc "~/cmdstan-2.16.0/bin/stanc")


Example
--------

::

    In [1]: %load_ext stanmagic

    In [2]: %%stan -f eight_schools.stan
            data {
                int<lower=0> J; // number of schools
                real y[J]; // estimated treatment effects
                real<lower=0> sigma[J]; // s.e. of effect estimates
              }
              parameters {
                real mu;
                real<lower=0> tau
                real eta[J];
              }
              transformed parameters {
                real theta[J];
                for (j in 1:J)
                theta[j] = mu + tau * eta[j];
              }
              model {
                target += normal_lpdf(eta | 0, 1);
                target += normal_lpdf(y | theta, sigma);
              }

    In [3]: model = pystan.StanModel(file='eight_schools.stan')


  SYNTAX ERROR, MESSAGE(S) FROM PARSER:
  error in 'eight_schools.stan' at line 10, column 5
  -------------------------------------------------
     8:     real mu;
     9:     real<lower=0> tau
    10:     real eta[J];
            ^
    11:   }
  -------------------------------------------------

  PARSER EXPECTED: ";"

::

        In [1]: %load_ext stanmagic

        In [2]: %%stan -f eight_schools.stan
                data {
                    int<lower=0> J; // number of schools
                    real y[J]; // estimated treatment effects
                    real<lower=0> sigma[J]; // s.e. of effect estimates
                  }
                  parameters {
                    real mu;
                    real<lower=0> tau;
                    real eta[J];
                  }
                  transformed parameters {
                    real theta[J];
                    for (j in 1:J)
                    theta[j] = mu + tau * eta[j];
                  }
                  model {
                    target += normal_lpdf(eta | 0, 1);
                    target += normal_lpdf(y | theta, sigma);
                  }

        In [3]: print(_stan_vars)

        {'stan_file': 'eight_schools.stan', 'stan_code': None, 'model_name': 'eight_schools_model'}


::

        In [1]: %load_ext stanmagic

        In [2]: %%stan
                data {
                    int<lower=0> J; // number of schools
                    real y[J]; // estimated treatment effects
                    real<lower=0> sigma[J]; // s.e. of effect estimates
                  }
                  parameters {
                    real mu;
                    real<lower=0> tau;
                    real eta[J];
                  }
                  transformed parameters {
                    real theta[J];
                    for (j in 1:J)
                    theta[j] = mu + tau * eta[j];
                  }
                  model {
                    target += normal_lpdf(eta | 0, 1);
                    target += normal_lpdf(y | theta, sigma);
                  }

        In [3]: model = pystan.StanModel(model_code=_stan_vars['stan_code'])

License
-------

*stan-jupyter-magic* is licensed under the MIT license. See the
license file for details.
